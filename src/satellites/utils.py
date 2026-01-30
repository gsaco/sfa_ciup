from __future__ import annotations

import contextlib
import gzip
import json
import math
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import rasterio
from rasterio.io import MemoryFile

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


def find_repo_root(start: Path | None = None) -> Path:
    start = Path.cwd() if start is None else Path(start)
    for parent in [start] + list(start.parents):
        if (parent / "src").exists() and (parent / "data").exists():
            return parent
    raise RuntimeError("Could not locate repo root. Run from within the repo.")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_json(path: Path, payload: dict) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _parse_ubigeo_plan_a(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    df = pd.read_excel(path)
    cols = {c.lower() for c in df.columns}
    expected = {"latitud", "longitud", "superficie"}
    if not expected.intersection(cols):
        return None
    return df


def _parse_ubigeo_fallback(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["ubigeo6"] = (
        pd.to_numeric(df["inei"], errors="coerce")
        .round()
        .astype("Int64")
        .astype("string")
        .str.zfill(6)
    )
    df = df[df["ubigeo6"].notna()].copy()
    df["ccdd"] = df["ubigeo6"].str.slice(0, 2)
    df["ccpp"] = df["ubigeo6"].str.slice(2, 4)
    df["ccdi"] = df["ubigeo6"].str.slice(4, 6)

    out = pd.DataFrame(
        {
            "ubigeo6": df["ubigeo6"],
            "ccdd": df["ccdd"],
            "ccpp": df["ccpp"],
            "ccdi": df["ccdi"],
            "departamento": df.get("departamento"),
            "provincia": df.get("provincia"),
            "distrito": df.get("distrito"),
            "capital_lat": pd.to_numeric(df.get("latitude"), errors="coerce"),
            "capital_lon": pd.to_numeric(df.get("longitude"), errors="coerce"),
            "surface_km2": pd.to_numeric(df.get("superficie"), errors="coerce"),
        }
    )
    return out


def _validate_ubigeo(df: pd.DataFrame) -> pd.DataFrame:
    if "ubigeo6" not in df.columns:
        raise ValueError("UBIGEO data missing 'ubigeo6' column.")
    df = df.copy()
    df["ubigeo6"] = df["ubigeo6"].astype("string")
    if df["ubigeo6"].isna().any():
        raise ValueError("UBIGEO data has missing ubigeo6 values.")
    if not (df["ubigeo6"].str.len() == 6).all():
        raise ValueError("UBIGEO data has non-6-digit ubigeo6 entries.")
    if not df["ubigeo6"].is_unique:
        raise ValueError("UBIGEO data has duplicate ubigeo6 entries.")
    return df


def load_ubigeo(
    processed_path: Path,
    fallback_csv: Path,
    fallback_excel: Path | None = None,
    write_back: bool = True,
) -> pd.DataFrame:
    df = None
    if processed_path.exists():
        try:
            df = pd.read_parquet(processed_path)
        except Exception as exc:  # pragma: no cover - depends on parquet reader
            print(f"[ubigeo] Failed to read {processed_path}: {exc}")
            df = None
    if df is None or df.empty:
        df = _parse_ubigeo_plan_a(fallback_excel) if fallback_excel else None
        if df is None:
            if not fallback_csv.exists():
                raise FileNotFoundError(f"Missing ubigeo fallback file: {fallback_csv}")
            df = _parse_ubigeo_fallback(fallback_csv)
        if write_back:
            ensure_dir(processed_path.parent)
            df.to_parquet(processed_path, index=False)
    return _validate_ubigeo(df)


@contextlib.contextmanager
def _open_raster(path: Path, gzip_enabled: bool = False):
    if gzip_enabled:
        with gzip.open(path, "rb") as handle:
            data = handle.read()
        with MemoryFile(data) as memfile:
            with memfile.open() as src:
                yield src
    else:
        with rasterio.open(path) as src:
            yield src


def raster_info(path: Path, gzip_enabled: bool = False) -> dict:
    with _open_raster(path, gzip_enabled=gzip_enabled) as src:
        return {
            "crs": src.crs,
            "bounds": src.bounds,
            "res": src.res,
            "nodata": src.nodata,
            "dtype": src.dtypes[0] if src.count else None,
            "count": src.count,
            "shape": (src.height, src.width),
        }


def _scale_offsets(ds: rasterio.io.DatasetReader) -> tuple[np.ndarray, np.ndarray]:
    scales = ds.scales if ds.scales else [1.0] * ds.count
    offsets = ds.offsets if ds.offsets else [0.0] * ds.count
    scales = np.array([1.0 if s is None else s for s in scales], dtype="float64")
    offsets = np.array([0.0 if o is None else o for o in offsets], dtype="float64")
    return scales, offsets


def sample_raster_points(
    path: Path,
    coords: list[tuple[float, float]],
    gzip_enabled: bool = False,
) -> np.ndarray:
    if not coords:
        return np.empty((0, 0), dtype="float64")
    with _open_raster(path, gzip_enabled=gzip_enabled) as ds:
        samples = np.stack(list(ds.sample(coords)))
        scales, offsets = _scale_offsets(ds)
        values = samples.astype("float64") * scales.reshape(1, -1) + offsets.reshape(1, -1)
        if ds.nodata is not None:
            values = np.where(samples == ds.nodata, np.nan, values)
        return values


def sum_with_nan(arrays: Iterable[np.ndarray]) -> np.ndarray:
    arrays = list(arrays)
    if not arrays:
        return np.array([], dtype="float64")
    total = np.zeros_like(arrays[0], dtype="float64")
    nan_mask = np.zeros_like(arrays[0], dtype=bool)
    for arr in arrays:
        nan_mask |= np.isnan(arr)
        total += np.nan_to_num(arr, nan=0.0)
    total[nan_mask] = np.nan
    return total


def missingness_table(df: pd.DataFrame) -> pd.DataFrame:
    total = len(df)
    missing = df.isna().sum()
    out = pd.DataFrame(
        {
            "column": missing.index,
            "missing_count": missing.values,
            "missing_pct": (missing.values / total * 100.0) if total else 0.0,
        }
    )
    return out.sort_values("missing_pct", ascending=False).reset_index(drop=True)


def select_numeric_columns(df: pd.DataFrame, exclude: Iterable[str] | None = None) -> list[str]:
    exclude = set(exclude or [])
    cols = [c for c in df.select_dtypes(include=["number"]).columns if c not in exclude]
    return cols


def outlier_table(
    df: pd.DataFrame,
    columns: Iterable[str],
    key: str = "ubigeo6",
    n: int = 20,
) -> pd.DataFrame:
    records = []
    for col in columns:
        if col not in df.columns:
            continue
        series = df[[key, col]].dropna()
        if series.empty:
            continue
        top = series.nlargest(n, col)
        bottom = series.nsmallest(n, col)
        for direction, subset in [("top", top), ("bottom", bottom)]:
            for rank, row in enumerate(subset.itertuples(index=False), start=1):
                records.append({"feature": col, "direction": direction, "rank": rank, key: row[0], "value": row[1]})
    return pd.DataFrame.from_records(records)


def coverage_report(
    features: pd.DataFrame,
    ubigeo: pd.DataFrame,
    key: str = "ubigeo6",
) -> tuple[pd.DataFrame, list[str]]:
    ubigeo_keys = set(ubigeo[key].dropna().astype(str))
    feature_keys = set(features[key].dropna().astype(str))
    matched = ubigeo_keys & feature_keys
    missing = sorted(ubigeo_keys - feature_keys)
    extra = sorted(feature_keys - ubigeo_keys)
    report = pd.DataFrame(
        [
            {"metric": "ubigeo_total", "value": len(ubigeo_keys)},
            {"metric": "feature_rows", "value": len(features)},
            {"metric": "matched_keys", "value": len(matched)},
            {"metric": "missing_keys", "value": len(missing)},
            {"metric": "extra_keys", "value": len(extra)},
        ]
    )
    return report, missing


def plot_missingness(table: pd.DataFrame, out_path: Path, title: str) -> None:
    if table.empty:
        return
    plt.figure(figsize=(max(6, len(table) * 0.4), 4))
    sns.barplot(data=table, x="column", y="missing_pct", color="#4C72B0")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Missing (%)")
    plt.title(title)
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()


def plot_hist_ecdf(df: pd.DataFrame, columns: list[str], out_path: Path, title: str) -> None:
    columns = [c for c in columns if c in df.columns]
    if not columns:
        return
    rows = 2
    cols = len(columns)
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 6), squeeze=False)
    for idx, col in enumerate(columns):
        sns.histplot(df[col], ax=axes[0, idx], kde=False, color="#55A868")
        axes[0, idx].set_title(f"{col} distribution")
        sns.ecdfplot(df[col], ax=axes[1, idx], color="#C44E52")
        axes[1, idx].set_title(f"{col} ECDF")
    fig.suptitle(title, y=1.02)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_corr_heatmap(corr: pd.DataFrame, out_path: Path, title: str) -> None:
    if corr.empty:
        return
    plt.figure(figsize=(max(6, 0.6 * len(corr)), max(4, 0.6 * len(corr))))
    sns.heatmap(corr, cmap="coolwarm", annot=False, center=0)
    plt.title(title)
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()


def safe_read_parquet(path: Path, required: bool = False) -> pd.DataFrame | None:
    if not path.exists():
        if required:
            raise FileNotFoundError(f"Missing parquet: {path}")
        return None
    try:
        return pd.read_parquet(path)
    except Exception as exc:
        if required:
            raise
        print(f"[parquet] Failed to read {path}: {exc}")
        return None


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
