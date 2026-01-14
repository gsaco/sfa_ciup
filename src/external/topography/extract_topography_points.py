#!/usr/bin/env python3
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from rasterio.windows import Window


REPO_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = REPO_ROOT / "data" / "external" / "raw" / "topography" / "copernicus_cog30_tiles"
PROCESSED_DIR = REPO_ROOT / "data" / "external" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

UBIGEO_PATH = REPO_ROOT / "data" / "external" / "processed" / "ubigeo_district_capitals.parquet"


def tile_name(lat: float, lon: float) -> str:
    lat_floor = math.floor(lat)
    lon_floor = math.floor(lon)
    lat_prefix = "N" if lat_floor >= 0 else "S"
    lon_prefix = "E" if lon_floor >= 0 else "W"
    return (
        f"Copernicus_DSM_COG_30_{lat_prefix}{abs(lat_floor):02d}_00_"
        f"{lon_prefix}{abs(lon_floor):03d}_00_DEM"
    )


def slope_from_window(window: np.ndarray, dx: float, dy: float) -> float:
    if window.shape != (3, 3):
        return float("nan")
    if np.isnan(window[1, 1]):
        return float("nan")
    dzdx = (window[1, 2] - window[1, 0]) / (2 * dx)
    dzdy = (window[2, 1] - window[0, 1]) / (2 * dy)
    if np.isnan(dzdx) or np.isnan(dzdy):
        return float("nan")
    slope_rad = math.atan(math.sqrt(dzdx ** 2 + dzdy ** 2))
    return math.degrees(slope_rad)


def main() -> None:
    if not UBIGEO_PATH.exists():
        raise FileNotFoundError(f"Missing ubigeo capitals: {UBIGEO_PATH}")

    ubigeo = pd.read_parquet(UBIGEO_PATH)
    points = ubigeo.dropna(subset=["capital_lat", "capital_lon"]).copy()
    points["tile"] = [
        tile_name(lat, lon) for lat, lon in zip(points["capital_lat"], points["capital_lon"])
    ]

    results = []

    for tile, group in points.groupby("tile"):
        tile_path = RAW_DIR / f"{tile}.tif"
        if not tile_path.exists():
            for _, row in group.iterrows():
                results.append(
                    {
                        "ubigeo6": row["ubigeo6"],
                        "elev_m": float("nan"),
                        "slope_deg": float("nan"),
                        "ruggedness": float("nan"),
                    }
                )
            continue

        with rasterio.open(tile_path) as ds:
            xres, yres = ds.res
            for _, row in group.iterrows():
                lon = float(row["capital_lon"])
                lat = float(row["capital_lat"])
                try:
                    r, c = ds.index(lon, lat)
                except Exception:
                    results.append(
                        {
                            "ubigeo6": row["ubigeo6"],
                            "elev_m": float("nan"),
                            "slope_deg": float("nan"),
                            "ruggedness": float("nan"),
                        }
                    )
                    continue

                elev = ds.read(1, window=Window(c, r, 1, 1), boundless=True, fill_value=np.nan)[0, 0]
                window = ds.read(1, window=Window(c - 1, r - 1, 3, 3), boundless=True, fill_value=np.nan)

                dx = abs(xres) * 111320 * math.cos(math.radians(lat))
                dy = abs(yres) * 111320
                slope = slope_from_window(window, dx, dy)
                rugged = float(np.nanstd(window))

                results.append(
                    {
                        "ubigeo6": row["ubigeo6"],
                        "elev_m": float(elev) if np.isfinite(elev) else float("nan"),
                        "slope_deg": slope,
                        "ruggedness": rugged,
                    }
                )

    output = pd.DataFrame(results)
    out_path = PROCESSED_DIR / "topography_district_features.parquet"
    output.to_parquet(out_path, index=False)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
