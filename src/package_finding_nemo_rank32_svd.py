import json
import os
import re
import zipfile
from pathlib import Path

import torch
from safetensors import safe_open
from safetensors.torch import save_file


WORK_DIR = Path("/kaggle/working")
BASE_MODEL_DIR = Path("/kaggle/input/models/metric/nemotron-3-nano-30b-a3b-bf16/transformers/default/1")
OUT_ZIP = WORK_DIR / "submission.zip"
OUT_ADAPTER = WORK_DIR / "adapter_model.safetensors"
OUT_CONFIG = WORK_DIR / "adapter_config.json"

VARIANCE_RETAINED = 0.92
MIN_RANK_RATIO = 0.25
SAVE_FP16 = True
MAX_RANK = 32


def find_adapter_dir() -> Path:
    candidates = [
        Path("/kaggle/input/datasets/assiaben/adapter-v32-epoch-3/adapter"),
        Path("/kaggle/input/adapter-v32-epoch-3/adapter"),
        Path("/kaggle/input/adapter"),
    ]
    for path in candidates:
        if (path / "adapter_config.json").exists() and (path / "adapter_model.safetensors").exists():
            return path
    for cfg_path in Path("/kaggle/input").rglob("adapter_config.json"):
        if (cfg_path.parent / "adapter_model.safetensors").exists():
            return cfg_path.parent
    raise FileNotFoundError("No adapter_config.json + adapter_model.safetensors pair found under /kaggle/input")


def load_safetensors(path: Path) -> dict[str, torch.Tensor]:
    tensors = {}
    with safe_open(path, framework="pt", device="cpu") as f:
        for key in f.keys():
            tensors[key] = f.get_tensor(key)
    return tensors


def load_model_shapes(model_dir: Path) -> set[str]:
    keys = set()
    for file_path in model_dir.glob("*.safetensors"):
        with safe_open(file_path, framework="pt", device="cpu") as f:
            keys.update(f.keys())
    return keys


def rename_key(key: str) -> str:
    return key.replace("base_model.model.model", "base_model.model.backbone")


def compressed_rank(singular_values: torch.Tensor, original_rank: int) -> int:
    energy = torch.cumsum(singular_values.square(), dim=0) / torch.sum(singular_values.square())
    variance_rank = int(torch.searchsorted(energy, torch.tensor(VARIANCE_RETAINED)).item()) + 1
    floor_rank = max(1, int(original_rank * MIN_RANK_RATIO))
    return min(MAX_RANK, max(floor_rank, variance_rank))


def compress_lora_pair(a: torch.Tensor, b: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    original_rank = min(a.shape[0], b.shape[1])
    merged = b.float() @ a.float()
    u, s, vh = torch.linalg.svd(merged, full_matrices=False)
    rank = compressed_rank(s, original_rank)

    s_sqrt = torch.sqrt(s[:rank])
    new_b = u[:, :rank] * s_sqrt.unsqueeze(0)
    new_a = s_sqrt.unsqueeze(1) * vh[:rank, :]
    if SAVE_FP16:
        new_a = new_a.half()
        new_b = new_b.half()
    return new_a.contiguous(), new_b.contiguous()


def convert_adapter(adapter_dir: Path) -> None:
    tensors = load_safetensors(adapter_dir / "adapter_model.safetensors")
    model_keys = load_model_shapes(BASE_MODEL_DIR)

    out = {}
    base_keys = sorted({re.sub(r"\.lora_[AB]\.weight$", "", key) for key in tensors})
    for base in base_keys:
        a = tensors.get(f"{base}.lora_A.weight")
        b = tensors.get(f"{base}.lora_B.weight")
        if a is None or b is None:
            continue

        renamed_base = rename_key(base)
        target_weight_key = renamed_base.replace("base_model.model.", "") + ".weight"
        if target_weight_key not in model_keys and renamed_base == base:
            continue

        new_a, new_b = compress_lora_pair(a, b)
        out[f"{renamed_base}.lora_A.weight"] = new_a
        out[f"{renamed_base}.lora_B.weight"] = new_b

    if not out:
        raise RuntimeError("No LoRA tensors were converted")
    save_file(out, OUT_ADAPTER)


def write_config(adapter_dir: Path) -> None:
    config = json.loads((adapter_dir / "adapter_config.json").read_text())
    config.update(
        {
            "base_model_name_or_path": "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16",
            "inference_mode": True,
            "lora_dropout": 0.0,
            "r": MAX_RANK,
            "rank_pattern": {},
            "alpha_pattern": {},
        }
    )
    config["target_modules"] = [
        "k_proj",
        "o_proj",
        "in_proj",
        "q_proj",
        "up_proj",
        "v_proj",
        "down_proj",
        "out_proj",
    ]
    OUT_CONFIG.write_text(json.dumps(config, indent=2), encoding="utf-8")


def write_submission() -> None:
    if OUT_ZIP.exists():
        OUT_ZIP.unlink()
    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as zf:
        zf.write(OUT_CONFIG, "adapter_config.json")
        zf.write(OUT_ADAPTER, "adapter_model.safetensors")
    with zipfile.ZipFile(OUT_ZIP) as zf:
        names = sorted(zf.namelist())
    if names != ["adapter_config.json", "adapter_model.safetensors"]:
        raise RuntimeError(f"Unexpected zip contents: {names}")


def main() -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    adapter_dir = find_adapter_dir()
    write_config(adapter_dir)
    convert_adapter(adapter_dir)
    write_submission()
    print(
        json.dumps(
            {
                "adapter_dir": str(adapter_dir),
                "out_zip": str(OUT_ZIP),
                "zip_size_bytes": os.path.getsize(OUT_ZIP),
                "variance_retained": VARIANCE_RETAINED,
                "min_rank_ratio": MIN_RANK_RATIO,
                "max_rank": MAX_RANK,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
