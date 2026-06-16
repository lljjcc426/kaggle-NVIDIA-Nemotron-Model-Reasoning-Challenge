import json
import os
import zipfile
from pathlib import Path


ADAPTER_DIR = Path("/kaggle/input/datasets/assiabenazzouz/adappter-v32-epoch-5/adapter")
OUT_ZIP = Path("/kaggle/working/submission.zip")
REQUIRED_FILES = ("adapter_config.json", "adapter_model.safetensors")


def validate_adapter(adapter_dir: Path) -> dict:
    missing = [name for name in REQUIRED_FILES if not (adapter_dir / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing adapter files: {missing}")

    config = json.loads((adapter_dir / "adapter_config.json").read_text())
    rank = int(config.get("r", config.get("rank", 999)))
    if rank > 32:
        raise ValueError(f"LoRA rank must be <= 32 for this competition, got {rank}")
    if str(config.get("peft_type", "")).upper() != "LORA":
        raise ValueError(f"Expected PEFT LORA adapter, got {config.get('peft_type')}")
    return config


def write_submission(adapter_dir: Path, out_zip: Path) -> None:
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    if out_zip.exists():
        out_zip.unlink()

    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as zf:
        for name in REQUIRED_FILES:
            zf.write(adapter_dir / name, name)

    with zipfile.ZipFile(out_zip) as zf:
        names = sorted(zf.namelist())
    if names != sorted(REQUIRED_FILES):
        raise RuntimeError(f"Unexpected zip contents: {names}")


def main() -> None:
    config = validate_adapter(ADAPTER_DIR)
    write_submission(ADAPTER_DIR, OUT_ZIP)
    size_mb = os.path.getsize(OUT_ZIP) / 1024 / 1024
    print(
        json.dumps(
            {
                "adapter_dir": str(ADAPTER_DIR),
                "out_zip": str(OUT_ZIP),
                "zip_size_mb": round(size_mb, 3),
                "rank": int(config.get("r", config.get("rank", -1))),
                "target_modules": config.get("target_modules"),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
