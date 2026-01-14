#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import rasterio


REPO_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = REPO_ROOT / "data" / "external" / "raw" / "temperature"
PROCESSED_DIR = REPO_ROOT / "data" / "external" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

UBIGEO_PATH = REPO_ROOT / "data" / "external" / "processed" / "ubigeo_district_capitals.parquet"


def sample_annual_mean(path: Path, var_name: str, points: list[tuple[float, float]]) -> np.ndarray:
    dataset_path = None
    with rasterio.open(path) as src:
        if src.subdatasets:
            for sub in src.subdatasets:
                if sub.endswith(f":{var_name}"):
                    dataset_path = sub
                    break
    if dataset_path:
        with rasterio.open(dataset_path) as ds:
            return _sample_dataset(ds, points)
    with rasterio.open(path) as ds:
        return _sample_dataset(ds, points)


def _sample_dataset(ds: rasterio.io.DatasetReader, points: list[tuple[float, float]]) -> np.ndarray:
    samples = np.stack(list(ds.sample(points)))
    scales = ds.scales if ds.scales else [1.0] * ds.count
    offsets = ds.offsets if ds.offsets else [0.0] * ds.count
    if scales and scales[0] is None:
        scales = [1.0] * ds.count
    if offsets and offsets[0] is None:
        offsets = [0.0] * ds.count
    scales = np.array(scales, dtype="float64").reshape(1, -1)
    offsets = np.array(offsets, dtype="float64").reshape(1, -1)
    values = samples * scales + offsets
    if ds.nodata is not None:
        values = np.where(values == ds.nodata, np.nan, values)
    return np.nanmean(values, axis=1)


def main() -> None:
    if not UBIGEO_PATH.exists():
        raise FileNotFoundError(f"Missing ubigeo capitals: {UBIGEO_PATH}")

    ubigeo = pd.read_parquet(UBIGEO_PATH)
    points = list(zip(ubigeo["capital_lon"].astype(float), ubigeo["capital_lat"].astype(float)))

    outputs = {"ubigeo6": ubigeo["ubigeo6"]}

    for year in [2023, 2024]:
        tmax_path = RAW_DIR / f"terraclimate_tmax_{year}_peru.nc"
        tmin_path = RAW_DIR / f"terraclimate_tmin_{year}_peru.nc"
        if not tmax_path.exists() or not tmin_path.exists():
            raise FileNotFoundError("Missing TerraClimate NCSS files for year {}".format(year))

        tmax = sample_annual_mean(tmax_path, "tmax", points)
        tmin = sample_annual_mean(tmin_path, "tmin", points)
        tmean = (tmax + tmin) / 2.0

        outputs[f"tmax_{year}"] = tmax
        outputs[f"tmin_{year}"] = tmin
        outputs[f"tmean_{year}"] = tmean

    outputs["delta_tmean_24_23"] = outputs["tmean_2024"] - outputs["tmean_2023"]

    df = pd.DataFrame(outputs)
    out_path = PROCESSED_DIR / "temperature_district_features_2023_2024.parquet"
    df.to_parquet(out_path, index=False)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
