#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import gzip
import numpy as np
import pandas as pd
import rasterio
from rasterio.io import MemoryFile


REPO_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = REPO_ROOT / "data" / "external" / "raw" / "chirps"
PROCESSED_DIR = REPO_ROOT / "data" / "external" / "processed"
UBIGEO_PATH = REPO_ROOT / "data" / "external" / "processed" / "ubigeo_district_capitals.parquet"
META_PATH = RAW_DIR / "metadata.json"

TARGET_YEAR = 2024


def load_meta() -> dict:
    if META_PATH.exists():
        return json.loads(META_PATH.read_text(encoding="utf-8"))
    return {}


def raster_path(year: int, month: int) -> Path:
    return RAW_DIR / "monthly_tifs" / str(year) / f"chirps-v2.0.{year}.{month:02d}.tif.gz"


def sample_raster(path: Path, coords: list[tuple[float, float]]) -> np.ndarray:
    with gzip.open(path, "rb") as handle:
        data = handle.read()
    with MemoryFile(data) as memfile:
        with memfile.open() as src:
            samples = list(src.sample(coords))
    return np.array([val[0] for val in samples], dtype="float64")


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    if not UBIGEO_PATH.exists():
        raise FileNotFoundError(f"Missing UBIGEO capitals: {UBIGEO_PATH}")

    ubigeo = pd.read_parquet(UBIGEO_PATH)
    coords = list(zip(ubigeo["capital_lon"].astype(float), ubigeo["capital_lat"].astype(float)))

    # 2024 totals
    prcp_total_2024 = np.zeros(len(ubigeo), dtype="float64")
    prcp_wet = np.zeros(len(ubigeo), dtype="float64")
    prcp_dry = np.zeros(len(ubigeo), dtype="float64")

    wet_months = {11, 12, 1, 2, 3}
    dry_months = {5, 6, 7, 8, 9}

    for month in range(1, 13):
        path = raster_path(TARGET_YEAR, month)
        if not path.exists():
            raise FileNotFoundError(f"Missing raster: {path}")
        values = sample_raster(path, coords)
        prcp_total_2024 += values
        if month in wet_months:
            prcp_wet += values
        if month in dry_months:
            prcp_dry += values

    meta = load_meta()
    baseline_start = meta.get("baseline_start", 1991)
    baseline_end = meta.get("baseline_end", 2020)

    # Baseline
    baseline_years = []
    for year in range(baseline_start, baseline_end + 1):
        yearly_total = np.zeros(len(ubigeo), dtype="float64")
        for month in range(1, 13):
            path = raster_path(year, month)
            if not path.exists():
                raise FileNotFoundError(f"Missing raster: {path}")
            values = sample_raster(path, coords)
            yearly_total += values
        baseline_years.append(yearly_total)

    baseline_stack = np.vstack(baseline_years)
    baseline_mean = baseline_stack.mean(axis=0)
    baseline_std = baseline_stack.std(axis=0, ddof=1)

    prcp_total_anom = prcp_total_2024 - baseline_mean
    prcp_total_z = np.where(baseline_std > 0, prcp_total_anom / baseline_std, np.nan)

    out = pd.DataFrame(
        {
            "ubigeo6": ubigeo["ubigeo6"],
            "prcp_2024_total": prcp_total_2024,
            "prcp_2024_wet": prcp_wet,
            "prcp_2024_dry": prcp_dry,
            "prcp_baseline_mean": baseline_mean,
            "prcp_baseline_sd": baseline_std,
            "prcp_total_anom": prcp_total_anom,
            "prcp_total_z": prcp_total_z,
        }
    )

    out_path = PROCESSED_DIR / "chirps_district_features_2024.parquet"
    out.to_parquet(out_path, index=False)

    meta.update(
        {
            "target_year": TARGET_YEAR,
            "baseline_start": baseline_start,
            "baseline_end": baseline_end,
            "plan_used": meta.get("plan_used", "B"),
        }
    )
    (PROCESSED_DIR / "chirps_metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
