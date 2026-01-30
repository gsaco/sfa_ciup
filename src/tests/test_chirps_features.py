from pathlib import Path

import pandas as pd
import pytest


def read_parquet_or_skip(path: Path) -> pd.DataFrame:
    try:
        return pd.read_parquet(path)
    except OSError as exc:
        pytest.skip(f"Unable to read parquet {path}: {exc}")


def test_chirps_features_basic():
    path = Path("data/external/processed/chirps_district_features_2024.parquet")
    assert path.exists(), "Missing CHIRPS features parquet"
    df = read_parquet_or_skip(path)

    assert df["ubigeo6"].is_unique
    assert (df["prcp_2024_total"] >= 0).mean() > 0.95
    assert (df["prcp_baseline_mean"] >= 0).mean() > 0.95
    assert df["prcp_total_z"].isna().mean() < 0.05

    # Plausible range checks (mm/year)
    assert df["prcp_2024_total"].between(0, 10000).mean() > 0.95
