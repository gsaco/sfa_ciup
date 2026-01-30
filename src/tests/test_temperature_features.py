from pathlib import Path

import pandas as pd
import pytest


def read_parquet_or_skip(path: Path) -> pd.DataFrame:
    try:
        return pd.read_parquet(path)
    except OSError as exc:
        pytest.skip(f"Unable to read parquet {path}: {exc}")


def test_temperature_features_basic():
    path = Path("data/external/processed/temperature_district_features_2023_2024.parquet")
    assert path.exists(), "Missing temperature features parquet"

    df = read_parquet_or_skip(path)
    assert df["ubigeo6"].is_unique

    for col in ["tmean_2023", "tmean_2024", "delta_tmean_24_23"]:
        assert col in df.columns

    # Coverage and plausible ranges for Peru
    assert df["tmean_2023"].notna().mean() > 0.95
    assert df["tmean_2024"].notna().mean() > 0.95

    assert df["tmean_2023"].between(-20, 40).mean() > 0.95
    assert df["tmean_2024"].between(-20, 40).mean() > 0.95
    assert df["delta_tmean_24_23"].between(-10, 10).mean() > 0.95
