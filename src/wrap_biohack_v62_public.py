from __future__ import annotations

import json
import shutil
import zipfile
from pathlib import Path


INPUT_ROOT = Path("/kaggle/input")
OUTPUT_ZIP = Path("/kaggle/working/submission.zip")
REPORT = Path("/kaggle/working/wrap_biohack_v62_public_report.json")
MIN_ZIP_BYTES = 2_000_000_000
EXPECTED = ["adapter_config.json", "adapter_model.safetensors"]


def inspect_zip(path: Path) -> dict:
    with zipfile.ZipFile(path, "r") as zf:
        names = zf.namelist()
        infos = {info.filename: {"file_size": info.file_size, "compress_size": info.compress_size} for info in zf.infolist()}
    return {"names": names, "infos": infos}


def main() -> None:
    candidates = sorted(INPUT_ROOT.rglob("submission.zip"), key=lambda p: ("nemotron-v62" not in str(p), len(str(p))))
    if not candidates:
        raise FileNotFoundError("No submission.zip found under /kaggle/input")

    inspected = []
    selected = None
    selected_info = None
    for path in candidates:
        size = path.stat().st_size
        try:
            info = inspect_zip(path)
            ok_layout = info["names"] == EXPECTED
        except Exception as exc:
            info = {"error": repr(exc)}
            ok_layout = False
        record = {"path": str(path), "size": size, "ok_layout": ok_layout, **info}
        inspected.append(record)
        if selected is None and size >= MIN_ZIP_BYTES and ok_layout:
            selected = path
            selected_info = record

    if selected is None:
        raise RuntimeError("No valid large root-level adapter submission.zip found")

    if OUTPUT_ZIP.exists():
        OUTPUT_ZIP.unlink()
    shutil.copy2(selected, OUTPUT_ZIP)

    report = {
        "variant": "wrap_biohack_v62_public_output_v1",
        "selected": selected_info,
        "output_zip": str(OUTPUT_ZIP),
        "output_size": OUTPUT_ZIP.stat().st_size,
        "inspected": inspected,
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2)[:12000])


if __name__ == "__main__":
    main()
