#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
from urllib.request import urlopen


REPO_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = REPO_ROOT / "data" / "external" / "raw" / "chirps"
RAW_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/tifs"
TARGET_YEAR = 2024
BASELINE_START = int(os.getenv("CHIRPS_BASELINE_START", "1991"))
BASELINE_END = int(os.getenv("CHIRPS_BASELINE_END", "2020"))
MAX_FILES = int(os.getenv("CHIRPS_MAX_FILES", "80"))

META_PATH = RAW_DIR / "metadata.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_meta() -> dict:
    if not META_PATH.exists():
        return {}
    try:
        return json.loads(META_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_meta(meta: dict) -> None:
    META_PATH.write_text(json.dumps(meta, indent=2), encoding="utf-8")


def file_url(year: int, month: int) -> str:
    return f"{BASE_URL}/chirps-v2.0.{year}.{month:02d}.tif.gz"


def download_file(url: str, out_path: Path) -> None:
    with urlopen(url) as response:
        data = response.read()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)


def main() -> None:
    meta = load_meta()
    files_meta = meta.get("files", {})

    baseline_years = list(range(BASELINE_START, BASELINE_END + 1))
    total_files = len(baseline_years) * 12
    baseline_note = ""
    if total_files > MAX_FILES:
        baseline_years = list(range(2015, 2020 + 1))
        baseline_note = "fallback_baseline_2015_2020_due_to_download_size"

    years = baseline_years + [TARGET_YEAR]
    for year in years:
        for month in range(1, 13):
            url = file_url(year, month)
            out_path = RAW_DIR / "monthly_tifs" / str(year) / f"chirps-v2.0.{year}.{month:02d}.tif.gz"

            if out_path.exists():
                current_hash = sha256(out_path)
                files_meta[out_path.as_posix()] = current_hash
                continue

            download_file(url, out_path)
            files_meta[out_path.as_posix()] = sha256(out_path)
            print(f"Downloaded {out_path}")

            meta.update(
                {
                    "base_url": BASE_URL,
                    "target_year": TARGET_YEAR,
                    "baseline_start": baseline_years[0],
                    "baseline_end": baseline_years[-1],
                    "baseline_note": baseline_note,
                    "accessed_at": dt.datetime.now().isoformat(timespec="seconds"),
                    "plan_used": "B",
                    "files": files_meta,
                }
            )
            save_meta(meta)

    meta.update(
        {
            "base_url": BASE_URL,
            "target_year": TARGET_YEAR,
            "baseline_start": baseline_years[0],
            "baseline_end": baseline_years[-1],
            "baseline_note": baseline_note,
            "accessed_at": dt.datetime.now().isoformat(timespec="seconds"),
            "plan_used": "B",
            "files": files_meta,
        }
    )
    save_meta(meta)
    print(f"Wrote {META_PATH}")


if __name__ == "__main__":
    main()
