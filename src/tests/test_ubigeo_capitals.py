import pandas as pd
from pathlib import Path


def test_ubigeo_capitals_basic():
    path = Path("data/external/processed/ubigeo_district_capitals.parquet")
    assert path.exists(), "Missing ubigeo_district_capitals.parquet"
    df = pd.read_parquet(path)

    assert df["ubigeo6"].notna().all()
    assert (df["ubigeo6"].str.len() == 6).all()
    assert df["ubigeo6"].is_unique

    lat = df["capital_lat"]
    lon = df["capital_lon"]
    assert lat.between(-20.5, 1.0).mean() > 0.95
    assert lon.between(-83.0, -67.0).mean() > 0.95

    surface = df["surface_km2"]
    share_positive = (surface > 0).mean()
    assert share_positive > 0.9
