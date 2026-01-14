#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(REPO_ROOT / "src"))

from ena.io import normalize_columns, read_csv


RAW_DIR = REPO_ROOT / "data" / "raw" / "ENA_2024"
INTERMEDIATE_DIR = REPO_ROOT / "data" / "intermediate"
MAP_PATH = INTERMEDIATE_DIR / "variable_map.json"

KEY_COLS = ["ANIO", "CCDD", "CCPP", "CCDI", "NSEGM", "ID_PROD", "UA"]


def coerce_keys(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    df = df.copy()
    for col in keys:
        if col in df.columns:
            df[col] = df[col].astype("string")
    return df


def main() -> None:
    if not MAP_PATH.exists():
        raise FileNotFoundError(f"Missing variable map: {MAP_PATH}")

    with MAP_PATH.open("r", encoding="utf-8") as handle:
        variable_map = json.load(handle)

    caratula_path = RAW_DIR / "973-Modulo1893" / "CARATULA.csv"
    cap200ab_path = RAW_DIR / "973-Modulo1895" / "03_CAP200AB.csv"

    caratula_cols = [
        "ANIO",
        "CCDD",
        "NOMBREDD",
        "CCPP",
        "NOMBREPV",
        "CCDI",
        "NOMBREDI",
        "NSEGM",
        "ID_PROD",
        "UA",
        "REGION",
        "ESTRATO",
        "FACTOR_PRODUCTOR",
        "LATITUD",
        "LONGITUD",
    ]
    crop_cols = [
        "ANIO",
        "CCDD",
        "CCPP",
        "CCDI",
        "NSEGM",
        "ID_PROD",
        "UA",
        "P204_COD",
        "P204_NOM",
        "P217_SUP_ha",
        "P219_CANT_1",
        "P219_CANT_2",
        "P220_1_VAL",
        "P220_2_VAL",
        "P220_3A_VAL",
        "P220_3B_VAL",
        "P212",
        "P213",
        "P214",
    ]

    caratula = read_csv(caratula_path, usecols=caratula_cols, low_memory=False)
    crop = read_csv(cap200ab_path, usecols=crop_cols, low_memory=False)
    caratula = normalize_columns(caratula)
    crop = normalize_columns(crop)
    caratula = coerce_keys(caratula, KEY_COLS)
    crop = coerce_keys(crop, KEY_COLS)

    merged = crop.merge(caratula, on=KEY_COLS, how="left", validate="many_to_one")

    merged = merged.rename(columns=variable_map)
    output_path = INTERMEDIATE_DIR / "ena2024_schema.parquet"
    merged.to_parquet(output_path, index=False)

    print(f"Wrote {output_path}")
    print(f"Rows: {len(merged)} | Cols: {merged.shape[1]}")
    missing_keys = {col: float(merged[col].isna().mean()) for col in ["anio", "ccdd", "ccpp", "ccdi", "psu", "id_prod", "ua"] if col in merged.columns}
    print(f"Missing key share: {missing_keys}")


if __name__ == "__main__":
    sys.exit(main())
