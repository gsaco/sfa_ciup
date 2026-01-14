#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import hashlib
import json
import shutil
import urllib.parse
import urllib.request
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = REPO_ROOT / "data" / "external" / "raw" / "temperature"
RAW_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "http://thredds.northwestknowledge.net:8080/thredds/ncss/grid/TERRACLIMATE_ALL/data"

BBOX = {"north": 1.0, "south": -19.0, "west": -82.0, "east": -68.0}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, path: Path) -> dict[str, object]:
    if not path.exists():
        with urllib.request.urlopen(url, timeout=120) as resp, path.open("wb") as handle:
            shutil.copyfileobj(resp, handle)
    size = path.stat().st_size
    return {"path": path.as_posix(), "sha256": sha256(path), "size_bytes": size}


def build_url(var: str, year: int) -> str:
    filename = f"TerraClimate_{var}_{year}.nc"
    params = {
        "var": var,
        "north": BBOX["north"],
        "south": BBOX["south"],
        "west": BBOX["west"],
        "east": BBOX["east"],
        "accept": "netcdf",
    }
    return f"{BASE_URL}/{filename}?{urllib.parse.urlencode(params)}"


def main() -> None:
    access_date = dt.datetime.now().isoformat(timespec="seconds")
    entries = []

    for year in [2023, 2024]:
        for var in ["tmax", "tmin"]:
            url = build_url(var, year)
            out_path = RAW_DIR / f"terraclimate_{var}_{year}_peru.nc"
            info = download(url, out_path)
            info.update({"var": var, "year": year, "url": url, "accessed": access_date})
            entries.append(info)

    meta = {
        "source": "TerraClimate THREDDS NCSS",
        "bbox": BBOX,
        "accessed": access_date,
        "files": entries,
    }

    meta_path = RAW_DIR / "metadata.json"
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {meta_path}")


if __name__ == "__main__":
    main()
