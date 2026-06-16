from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import torch

WHEEL_DIR_CANDIDATES = [
    Path("/kaggle/input/datasets/michaelkong537/wheel-linux/wheelhouse"),
    Path("/kaggle/input/wheel-linux/wheelhouse"),
]
BASE_MODEL_CANDIDATES = [
    Path("/kaggle/input/models/metric/nemotron-3-nano-30b-a3b-bf16/transformers/default/1"),
    Path("/kaggle/input/metric/nemotron-3-nano-30b-a3b-bf16/transformers/default/1"),
    Path("/kaggle/input/nemotron-3-nano-30b-a3b-bf16/transformers/default/1"),
    Path("/kaggle/input/nemotron-3-nano-30b-a3b-bf16"),
]
BASE_MODEL_REFERENCE = "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16"
SOURCE_ADAPTER_CANDIDATES = [
    Path("/kaggle/input/huikang-default20-adapter-mirror-20260614"),
    Path("/kaggle/input/datasets/llccqq624/huikang-default20-adapter-mirror-20260614"),
    Path("/kaggle/input/models/huikang/nemotron-adapter/transformers/default/20"),
    Path("/kaggle/input/huikang/nemotron-adapter/transformers/default/20"),
    Path("/kaggle/input/nemotron-adapter/transformers/default/20"),
    Path("/kaggle/input/nemotron-adapter"),
]
OUTPUT_DIR = Path("/kaggle/working/nemotron-adapter-refine-psf-clean")
ZIP_PATH = Path("/kaggle/working/submission.zip")

FORCED_FUSED_RANK = 32
PSF_LAYER_DENOM = 48.0
PSF_V_START_COEF = 0.5
PSF_V_END_COEF = 2.5


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def first_existing(candidates: list[Path], label: str) -> Path:
    for path in candidates:
        if path.exists():
            print(f"[path] {label}: {path}")
            return path
    raise FileNotFoundError(f"Could not find {label}. Tried: {[str(p) for p in candidates]}")


def discover_adapter() -> Path:
    for path in SOURCE_ADAPTER_CANDIDATES:
        if (path / "adapter_config.json").exists() and (path / "adapter_model.safetensors").exists():
            print(f"[path] source_adapter: {path}")
            return path

    hits = []
    for cfg in Path("/kaggle/input").rglob("adapter_config.json"):
        folder = cfg.parent
        if not (folder / "adapter_model.safetensors").exists():
            continue
        score = 0
        low = str(folder).lower()
        for token in ["huikang", "nemotron", "adapter", "default", "20"]:
            if token in low:
                score += 10
        score -= len(str(folder)) / 1000
        hits.append((score, folder))
    if hits:
        hits.sort(reverse=True, key=lambda row: row[0])
        print(f"[path] source_adapter discovered: {hits[0][1]}")
        return hits[0][1]
    raise FileNotFoundError("Could not discover a source adapter under /kaggle/input")


def discover_base_model() -> str:
    for path in BASE_MODEL_CANDIDATES:
        if (path / "config.json").exists():
            print(f"[path] base_model: {path}")
            return str(path)

    hits = []
    for cfg in Path("/kaggle/input").rglob("config.json"):
        folder = cfg.parent
        low = str(folder).lower()
        if "adapter" in low:
            continue
        if "nemotron" in low and ("30b" in low or "nano" in low or "a3b" in low):
            score = 100 - len(str(folder)) / 1000
            hits.append((score, folder))
    if hits:
        hits.sort(reverse=True, key=lambda row: row[0])
        print(f"[path] base_model discovered: {hits[0][1]}")
        return str(hits[0][1])
    print(f"[path] base_model reference: {BASE_MODEL_REFERENCE}")
    return BASE_MODEL_REFERENCE


def install_offline_tinker() -> None:
    wheel_dir = first_existing(WHEEL_DIR_CANDIDATES, "wheelhouse")
    cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--no-index",
        f"--find-links={wheel_dir}",
        "tinker-cookbook",
        "tinker",
        "chz",
    ]
    print("[install]", " ".join(str(x) for x in cmd))
    subprocess.run(cmd, check=True)


def patch_tinker_merge() -> None:
    import tinker_cookbook.weights._adapter as adapter_mod

    stats = {
        "compressed_fused_modules": 0,
        "psf_fused_modules": 0,
        "standard_fused_modules": 0,
        "rank_in_values": [],
        "rank_out_values": [],
        "psf_filter_min": None,
        "psf_filter_max": None,
        "psf_samples": [],
    }

    def extract_layer_idx(name: str) -> int:
        match = re.search(r"\.layers\.(\d+)\.", name)
        if match:
            return int(match.group(1))
        return 0

    def fast_exact_svd(
        b_tensor: torch.Tensor,
        a_tensor: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        q_b, r_b = torch.linalg.qr(b_tensor.float())
        q_a, r_a = torch.linalg.qr(a_tensor.float().T)
        inner = r_b @ r_a.T
        u_inner, s, vh_inner = torch.linalg.svd(inner, full_matrices=False)
        u = q_b @ u_inner
        vh = vh_inner @ q_a.T
        return u, s, vh

    def compress_lora_pair_to_rank(
        b_tensor: torch.Tensor,
        a_tensor: torch.Tensor,
        rank: int,
        comp_slices,
        component_order,
        layer_idx: int,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        if b_tensor.ndim != 2 or a_tensor.ndim != 2:
            raise ValueError(f"Expected 2D LoRA pair, got B={tuple(b_tensor.shape)} A={tuple(a_tensor.shape)}")
        if b_tensor.shape[1] != a_tensor.shape[0]:
            raise ValueError(f"LoRA rank mismatch, got B={tuple(b_tensor.shape)} A={tuple(a_tensor.shape)}")

        u, s, vh = fast_exact_svd(b_tensor, a_tensor)
        rank = min(int(rank), int(s.numel()))
        u = u[:, :rank]
        s = s[:rank].clone()
        vh = vh[:rank, :]

        rank_in = int(b_tensor.shape[1])
        is_qkv = any("q_proj" in comp.lower() for comp in component_order)
        if is_qkv:
            layer_ratio = min(float(layer_idx), PSF_LAYER_DENOM) / PSF_LAYER_DENOM
            start_val = 1.0 - PSF_V_START_COEF * (layer_ratio ** 2)
            end_val = 1.0 + PSF_V_END_COEF * (layer_ratio ** 2)
            idx = torch.arange(rank, device=s.device, dtype=s.dtype)
            psf_filter = start_val + (end_val - start_val) * (idx / max(1, rank - 1))
            for slice_idx, (row_start, row_end, _component_rank) in enumerate(comp_slices):
                comp_name = component_order[slice_idx].lower()
                if "v_proj" in comp_name:
                    u[row_start:row_end, :] = u[row_start:row_end, :] * psf_filter.unsqueeze(0)

            stats["psf_fused_modules"] += 1
            filter_min = float(psf_filter.min().detach().cpu())
            filter_max = float(psf_filter.max().detach().cpu())
            if stats["psf_filter_min"] is None or filter_min < stats["psf_filter_min"]:
                stats["psf_filter_min"] = filter_min
            if stats["psf_filter_max"] is None or filter_max > stats["psf_filter_max"]:
                stats["psf_filter_max"] = filter_max
            if len(stats["psf_samples"]) < 12:
                stats["psf_samples"].append(
                    {
                        "layer_idx": layer_idx,
                        "filter_min": filter_min,
                        "filter_max": filter_max,
                        "component_order": list(component_order),
                    }
                )
        else:
            stats["standard_fused_modules"] += 1

        stats["compressed_fused_modules"] += 1
        stats["rank_in_values"].append(rank_in)
        stats["rank_out_values"].append(rank)

        sroot = torch.sqrt(s)
        b_new = u * sroot.unsqueeze(0)
        a_new = sroot.unsqueeze(1) * vh
        return b_new.to(b_tensor.dtype).contiguous(), a_new.to(a_tensor.dtype).contiguous()

    def patched_merge_fused_projections(
        fused_model_key: str,
        adapter_layer_prefix: str,
        components,
        model_state_shapes,
        peft_weights,
        target_modules,
        profile,
    ) -> int:
        fused_out_dim = model_state_shapes[fused_model_key][0]
        fused_target_name = fused_model_key.removesuffix(".weight").rsplit(".", 1)[-1]

        component_order = None
        for target, comps in profile.fused_projection_map:
            if target == fused_target_name:
                component_order = comps
                break
        if component_order is None:
            raise RuntimeError(f"Missing fused component order for {fused_model_key}")

        comp_by_name = {name: (lora_a, lora_b) for name, lora_a, lora_b in components}
        lora_a_parts = []
        comp_slices = []
        merged_rank = 0
        row_offset = 0

        for comp_name in component_order:
            if comp_name not in comp_by_name:
                raise RuntimeError(f"Missing component {comp_name!r} for {fused_model_key!r}")
            lora_a, lora_b = comp_by_name[comp_name]
            rank = int(lora_a.shape[0])
            out_dim = int(lora_b.shape[0])
            lora_a_parts.append(lora_a)
            comp_slices.append((row_offset, row_offset + out_dim, rank))
            row_offset += out_dim
            merged_rank += rank

        merged_lora_a = torch.cat(lora_a_parts, dim=0)
        merged_lora_b = torch.zeros(
            fused_out_dim,
            merged_rank,
            dtype=merged_lora_a.dtype,
            device=merged_lora_a.device,
        )

        rank_offset = 0
        for idx, (row_start, row_end, rank) in enumerate(comp_slices):
            _, lora_b = comp_by_name[component_order[idx]]
            merged_lora_b[row_start:row_end, rank_offset : rank_offset + rank] = lora_b
            rank_offset += rank

        final_rank = int(merged_rank)
        if merged_rank > FORCED_FUSED_RANK:
            merged_lora_b, merged_lora_a = compress_lora_pair_to_rank(
                merged_lora_b,
                merged_lora_a,
                FORCED_FUSED_RANK,
                comp_slices,
                component_order,
                extract_layer_idx(fused_model_key),
            )
            final_rank = int(merged_lora_a.shape[0])

        peft_target_key = f"{adapter_layer_prefix}.{fused_target_name}.weight"
        adapter_mod._add_peft_weight(peft_target_key, merged_lora_a, merged_lora_b, peft_weights, target_modules)
        return final_rank

    adapter_mod._merge_fused_projections = patched_merge_fused_projections
    patch_tinker_merge.stats = stats
    print("[patch] installed refine-psf-clean fused projection merge")


def main() -> None:
    source_adapter = discover_adapter()
    base_model = discover_base_model()

    install_offline_tinker()
    patch_tinker_merge()

    from tinker_cookbook import weights

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    print("[build] source_adapter", source_adapter)
    print("[build] base_model", base_model)
    weights.build_lora_adapter(
        base_model=base_model,
        adapter_path=str(source_adapter),
        output_path=str(OUTPUT_DIR),
    )

    required = ["adapter_config.json", "adapter_model.safetensors"]
    missing = [name for name in required if not (OUTPUT_DIR / name).exists()]
    if missing:
        raise FileNotFoundError(f"Build missing required files: {missing}")

    report = {
        "variant": "huikang_default20mirror_refine_psf_clean",
        "source_adapter": str(source_adapter),
        "base_model": str(base_model),
        "forced_fused_rank": FORCED_FUSED_RANK,
        "psf_layer_denom": PSF_LAYER_DENOM,
        "psf_v_start_coef": PSF_V_START_COEF,
        "psf_v_end_coef": PSF_V_END_COEF,
        "patch_stats": patch_tinker_merge.stats,
        "files": {
            name: {
                "size": (OUTPUT_DIR / name).stat().st_size,
                "sha256": sha256_file(OUTPUT_DIR / name),
            }
            for name in required
        },
    }
    (OUTPUT_DIR / "refine_psf_clean_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("[report]", json.dumps(report, indent=2))

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in required:
            zf.write(OUTPUT_DIR / name, arcname=name)

    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        names = zf.namelist()
        bad = zf.testzip()
    if bad is not None:
        raise RuntimeError(f"Zip integrity failed at {bad}")
    if names != required:
        raise RuntimeError(f"Unexpected zip layout: {names}")

    print("[zip] path", ZIP_PATH)
    print("[zip] size", ZIP_PATH.stat().st_size)
    print("[zip] sha256", sha256_file(ZIP_PATH))
    print("[zip] contents", names)


if __name__ == "__main__":
    main()
