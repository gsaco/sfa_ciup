from pathlib import Path

import pandas as pd
import pytest


def read_parquet_or_skip(path: Path) -> pd.DataFrame:
    try:
        return pd.read_parquet(path)
    except OSError as exc:
        pytest.skip(f"Unable to read parquet {path}: {exc}")


def test_topography_features_basic():
    path = Path("data/external/processed/topography_district_features.parquet")
    assert path.exists(), "Missing topography features parquet"

    df = read_parquet_or_skip(path)
    assert df["ubigeo6"].is_unique

    assert df["elev_m"].notna().mean() > 0.95
    assert df["slope_deg"].notna().mean() > 0.95
    assert df["ruggedness"].notna().mean() > 0.95

    assert df["elev_m"].between(-100, 7000).mean() > 0.95
    assert (df["slope_deg"] >= 0).mean() > 0.95
    assert (df["ruggedness"] >= 0).mean() > 0.95
