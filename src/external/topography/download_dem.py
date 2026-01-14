#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import shutil
import urllib.request
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = REPO_ROOT / "data" / "external" / "raw" / "topography"
TILES_DIR = RAW_DIR / "copernicus_cog30_tiles"
RAW_DIR.mkdir(parents=True, exist_ok=True)
TILES_DIR.mkdir(parents=True, exist_ok=True)

UBIGEO_PATH = REPO_ROOT / "data" / "external" / "processed" / "ubigeo_district_capitals.parquet"
BASE_URL = "https://copernicus-dem-90m.s3.amazonaws.com"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tile_name(lat: float, lon: float) -> str:
    lat_floor = math.floor(lat)
    lon_floor = math.floor(lon)
    lat_prefix = "N" if lat_floor >= 0 else "S"
    lon_prefix = "E" if lon_floor >= 0 else "W"
    return (
        f"Copernicus_DSM_COG_30_{lat_prefix}{abs(lat_floor):02d}_00_"
        f"{lon_prefix}{abs(lon_floor):03d}_00_DEM"
    )


def remote_size(url: str) -> int | None:
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=20) as resp:
            size = resp.headers.get("Content-Length")
            return int(size) if size else None
    except Exception:
        return None


def download(url: str, path: Path) -> None:
    expected = remote_size(url)
    if path.exists() and expected is not None:
        if path.stat().st_size == expected:
            return
    tmp_path = path.with_suffix(".tmp")
    with urllib.request.urlopen(url, timeout=120) as resp, tmp_path.open("wb") as handle:
        shutil.copyfileobj(resp, handle)
    tmp_path.replace(path)


def main() -> None:
    if not UBIGEO_PATH.exists():
        raise FileNotFoundError(f"Missing ubigeo capitals: {UBIGEO_PATH}")

    ubigeo = pd.read_parquet(UBIGEO_PATH)
    valid = ubigeo.dropna(subset=["capital_lat", "capital_lon"]).copy()
    valid["tile"] = [
        tile_name(lat, lon) for lat, lon in zip(valid["capital_lat"], valid["capital_lon"])
    ]
    tiles = sorted(valid["tile"].unique().tolist())

    access_date = dt.datetime.now().isoformat(timespec="seconds")
    entries = []

    for tile in tiles:
        url = f"{BASE_URL}/{tile}/{tile}.tif"
        out_path = TILES_DIR / f"{tile}.tif"
        download(url, out_path)
        entries.append(
            {
                "tile": tile,
                "url": url,
                "path": out_path.as_posix(),
                "sha256": sha256(out_path),
                "size_bytes": out_path.stat().st_size,
            }
        )

    meta = {
        "source": "Copernicus DEM GLO-90 (COG 1x1 degree tiles)",
        "accessed": access_date,
        "tile_count": len(tiles),
        "tiles": entries,
    }

    meta_path = RAW_DIR / "metadata.json"
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {meta_path}")


if __name__ == "__main__":
    main()
