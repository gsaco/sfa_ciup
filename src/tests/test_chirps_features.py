import pandas as pd
from pathlib import Path


def test_chirps_features_basic():
    path = Path("data/external/processed/chirps_district_features_2024.parquet")
    assert path.exists(), "Missing CHIRPS features parquet"
    df = pd.read_parquet(path)

    assert df["ubigeo6"].is_unique
    assert (df["prcp_2024_total"] >= 0).mean() > 0.95
    assert (df["prcp_baseline_mean"] >= 0).mean() > 0.95
    assert df["prcp_total_z"].isna().mean() < 0.05

    # Plausible range checks (mm/year)
    assert df["prcp_2024_total"].between(0, 10000).mean() > 0.95
