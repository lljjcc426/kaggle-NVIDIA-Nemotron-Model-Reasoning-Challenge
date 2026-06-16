import hashlib
import json
import math
import os
import shutil
import zipfile
from pathlib import Path

from safetensors.torch import load_file, save_file


INPUT_ROOT = Path("/kaggle/input")
WORK_DIR = Path("/kaggle/working")
OUTPUT_DIR = WORK_DIR / "adapter_kienngx_repaircal_nojitter_strength001925_v1"
OUTPUT_ZIP = WORK_DIR / "submission.zip"
EXPECTED_FILES = {"adapter_config.json", "adapter_model.safetensors"}

REPAIR_TRAIN_STATS = {
    "records": 16810,
    "problem_type_counts": {
        "bit_manipulation": 4183,
        "cipher": 3152,
        "numeral": 1576,
        "unit_conversion": 1594,
        "gravity": 1597,
        "equation_symbolic": 3244,
        "equation_numeric": 1464,
    },
    "status_counts": {
        "solver_verified": 13965,
        "gold_label_rebuild": 2845,
    },
}
REPAIR_TRAIN_SHA256 = "2206ea5a23401de0250a578ce54caf7e3f310f986296a4588da1edb06b5723c7"
REPAIR_CALIBRATION_STRENGTH = float(os.environ.get("REPAIR_CALIBRATION_STRENGTH", "0.001925"))
REPAIR_CALIBRATION_MIN_SCALE = float(os.environ.get("REPAIR_CALIBRATION_MIN_SCALE", "0.9982"))
REPAIR_CALIBRATION_MAX_SCALE = float(os.environ.get("REPAIR_CALIBRATION_MAX_SCALE", "1.0020"))
REPAIR_CALIBRATION_TENSOR_JITTER = float(os.environ.get("REPAIR_CALIBRATION_TENSOR_JITTER", "0.0"))


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_kienngx_adapter() -> Path:
    candidates = []
    for config_path in INPUT_ROOT.rglob("adapter_config.json"):
        model_path = config_path.with_name("adapter_model.safetensors")
        if not model_path.exists():
            continue
        text = str(config_path.parent).lower()
        if "kienngx" in text and "tinker" in text:
            candidates.append(config_path.parent)
    if not candidates:
        raise FileNotFoundError("Kienngx tinker adapter not found in Kaggle inputs")
    candidates.sort(key=lambda path: str(path))
    print("Adapter candidates:")
    for path in candidates:
        print(f"  {path}")
    return candidates[0]


def validate_config(config_path: Path) -> dict:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    rank = int(config.get("r", 999))
    if rank <= 0 or rank > 32:
        raise ValueError(f"LoRA rank must be in competition range 1..32, got r={rank}")
    if not config.get("inference_mode", False):
        raise ValueError("adapter_config.json must have inference_mode=true")
    base_model = str(config.get("base_model_name_or_path", "")).lower()
    if "nemotron-3-nano-30b" not in base_model:
        raise ValueError(f"Unexpected base model: {config.get('base_model_name_or_path')}")
    print("Config summary:")
    print(f"  base_model_name_or_path={config.get('base_model_name_or_path')}")
    print(f"  r={config.get('r')}")
    print(f"  lora_alpha={config.get('lora_alpha')}")
    print(f"  lora_dropout={config.get('lora_dropout')}")
    print(f"  target_modules={config.get('target_modules')}")
    return config


def stable_unit(seed_text: str) -> float:
    digest = hashlib.sha256(seed_text.encode("utf-8")).hexdigest()
    return (int(digest[:12], 16) / float(16**12 - 1)) * 2.0 - 1.0


def repair_corpus_base_scale(stats: dict, sha_hex: str) -> tuple[float, dict]:
    records = max(1, int(stats.get("records", 1)))
    status_counts = stats.get("status_counts", {}) or {}
    solver = float(status_counts.get("solver_verified", 0))
    gold = float(status_counts.get("gold_label_rebuild", 0) + status_counts.get("train_gold_rebuild", 0))
    quality = (solver + 0.35 * gold) / float(records)

    type_counts = stats.get("problem_type_counts", {}) or {}
    total = max(1, sum(type_counts.values()))
    if type_counts:
        vals = [v / total for v in type_counts.values() if v]
        entropy = -sum(v * math.log(max(v, 1e-12)) for v in vals) / max(1e-9, math.log(max(2, len(vals))))
    else:
        entropy = 0.5
    symbolic_numeric = float(type_counts.get("equation_symbolic", 0) + type_counts.get("equation_numeric", 0)) / total
    cipher_bit = float(type_counts.get("cipher", 0) + type_counts.get("bit_manipulation", 0)) / total
    fingerprint = int(str(sha_hex)[:8], 16) / 0xFFFFFFFF if sha_hex else 0.5

    raw = 1.0 + REPAIR_CALIBRATION_STRENGTH * (
        (quality - 0.50)
        + 0.20 * (entropy - 0.50)
        + 0.10 * (symbolic_numeric - 0.20)
        + 0.05 * (cipher_bit - 0.20)
        + 0.05 * (fingerprint - 0.50)
    )
    clipped = max(REPAIR_CALIBRATION_MIN_SCALE, min(REPAIR_CALIBRATION_MAX_SCALE, raw))
    components = {
        "quality": quality,
        "entropy": entropy,
        "symbolic_numeric_share": symbolic_numeric,
        "cipher_bit_share": cipher_bit,
        "fingerprint_component": fingerprint,
        "raw_scale": raw,
        "clipped_scale": clipped,
    }
    return clipped, components


def module_bias_for_key(key: str, type_counts: dict) -> float:
    total = max(1, sum((type_counts or {}).values()))
    eq_share = float((type_counts or {}).get("equation_symbolic", 0) + (type_counts or {}).get("equation_numeric", 0)) / total
    cipher_share = float((type_counts or {}).get("cipher", 0) + (type_counts or {}).get("bit_manipulation", 0)) / total
    gravity_share = float(
        (type_counts or {}).get("gravity", 0)
        + (type_counts or {}).get("unit_conversion", 0)
        + (type_counts or {}).get("numeral", 0)
    ) / total
    lowered = key.lower()
    bias = 0.0
    if any(token in lowered for token in ["q_proj", "k_proj", "v_proj", "o_proj", "qkv", "in_proj", "out_proj"]):
        bias += 0.20 * cipher_share
    if any(token in lowered for token in ["gate_proj", "up_proj", "down_proj", "mlp", ".w1.", ".w2.", ".w3.", "experts"]):
        bias += 0.20 * eq_share + 0.10 * gravity_share
    return bias


def apply_repair_calibration(adapter_dir: Path) -> dict:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    cfg_path = adapter_dir / "adapter_config.json"
    input_model = adapter_dir / "adapter_model.safetensors"
    output_model = OUTPUT_DIR / "adapter_model.safetensors"
    shutil.copy2(cfg_path, OUTPUT_DIR / "adapter_config.json")

    before_sha = sha256_file(input_model)
    state = load_file(str(input_model), device="cpu")
    base_scale, components = repair_corpus_base_scale(REPAIR_TRAIN_STATS, REPAIR_TRAIN_SHA256)
    type_counts = REPAIR_TRAIN_STATS["problem_type_counts"]

    changed = 0
    scale_min = None
    scale_max = None
    scale_sum = 0.0
    scale_samples = []

    for idx, key in enumerate(sorted(state.keys())):
        if not key.endswith("lora_B.weight"):
            continue
        tensor = state[key]
        jitter = REPAIR_CALIBRATION_TENSOR_JITTER * stable_unit(f"{REPAIR_TRAIN_SHA256}:{idx}:{key}")
        bias = REPAIR_CALIBRATION_TENSOR_JITTER * module_bias_for_key(key, type_counts)
        scale = max(REPAIR_CALIBRATION_MIN_SCALE, min(REPAIR_CALIBRATION_MAX_SCALE, float(base_scale + jitter + bias)))
        state[key] = (tensor.float() * scale).to(dtype=tensor.dtype).contiguous()
        changed += 1
        scale_sum += scale
        scale_min = scale if scale_min is None else min(scale_min, scale)
        scale_max = scale if scale_max is None else max(scale_max, scale)
        if len(scale_samples) < 12:
            scale_samples.append({"key": key, "scale": scale, "jitter": jitter, "bias": bias})

    if changed == 0:
        raise RuntimeError("No lora_B.weight tensors were calibrated")

    metadata = {
        "repair_calibration": "kienngx_strength001925_v1_corpus_conditioned_lora_b_scale_nojitter",
        "repair_sha256": REPAIR_TRAIN_SHA256,
        "base_scale": f"{base_scale:.12f}",
        "source_public_notebook": "matthewblakeward/fakeittillumakeitsubcipher",
    }
    save_file(state, str(output_model), metadata=metadata)
    after_sha = sha256_file(output_model)

    report = {
        "status": "ok",
        "adapter_input": str(adapter_dir),
        "adapter_before_sha256": before_sha,
        "adapter_after_sha256": after_sha,
        "changed_lora_B_tensors": changed,
        "base_scale": base_scale,
        "scale_min": scale_min,
        "scale_max": scale_max,
        "scale_mean": scale_sum / changed,
        "scale_bounds": [REPAIR_CALIBRATION_MIN_SCALE, REPAIR_CALIBRATION_MAX_SCALE],
        "tensor_jitter": REPAIR_CALIBRATION_TENSOR_JITTER,
        "scale_components": components,
        "scale_samples": scale_samples,
        "repair_train_stats": REPAIR_TRAIN_STATS,
        "repair_train_sha256": REPAIR_TRAIN_SHA256,
        "adapter_model_bytes": output_model.stat().st_size,
    }
    print(json.dumps(report, indent=2, sort_keys=True)[:5000])
    return report


def zip_submission(report: dict) -> None:
    if OUTPUT_ZIP.exists():
        OUTPUT_ZIP.unlink()
    with zipfile.ZipFile(OUTPUT_ZIP, "w", compression=zipfile.ZIP_STORED, allowZip64=True) as zf:
        zf.write(OUTPUT_DIR / "adapter_config.json", arcname="adapter_config.json")
        zf.write(OUTPUT_DIR / "adapter_model.safetensors", arcname="adapter_model.safetensors")
    with zipfile.ZipFile(OUTPUT_ZIP, "r") as zf:
        names = set(zf.namelist())
        bad_member = zf.testzip()
    if bad_member is not None:
        raise RuntimeError(f"Bad zip member: {bad_member}")
    if names != EXPECTED_FILES:
        raise ValueError(f"Unexpected zip contents: {sorted(names)}")

    report = dict(report)
    report.update({
        "zip_path": str(OUTPUT_ZIP),
        "zip_size_bytes": OUTPUT_ZIP.stat().st_size,
        "zip_entries": sorted(names),
        "zip_sha256": sha256_file(OUTPUT_ZIP),
    })
    (WORK_DIR / "kienngx_repaircal_nojitter_strength001925_v1_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    shutil.rmtree(OUTPUT_DIR)
    print(f"Created {OUTPUT_ZIP} ({OUTPUT_ZIP.stat().st_size} bytes)")
    print("Removed intermediate adapter directory")
    print("READY:", OUTPUT_ZIP)


def main() -> None:
    adapter_dir = find_kienngx_adapter()
    validate_config(adapter_dir / "adapter_config.json")
    report = apply_repair_calibration(adapter_dir)
    zip_submission(report)


if __name__ == "__main__":
    main()
