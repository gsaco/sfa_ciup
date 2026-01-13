#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(REPO_ROOT / "src"))

from ena.io import normalize_columns, read_csv


RAW_DIR = REPO_ROOT / "data" / "raw" / "ENA_2024"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
INTERMEDIATE_DIR = REPO_ROOT / "data" / "intermediate"

ID_COLS = ["anio", "ccdd", "ccpp", "ccdi", "psu", "id_prod", "ua"]


def coerce_keys(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    df = df.copy()
    for col in keys:
        if col in df.columns:
            df[col] = df[col].astype("string")
    return df


def main() -> None:
    features_path = PROCESSED_DIR / "ena2024_features.parquet"
    if not features_path.exists():
        raise FileNotFoundError(f"Missing features file: {features_path}")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    features = pd.read_parquet(features_path)
    features = coerce_keys(features, ID_COLS)

    cap1000_path = RAW_DIR / "973-Modulo1910" / "18_CAP1000.csv"
    cap200e_path = RAW_DIR / "973-Modulo1899" / "07_CAP200E.csv"
    cap300_path = RAW_DIR / "973-Modulo1900" / "08_CAP300AB.csv"

    cap1000_cols = [
        "ANIO",
        "CCDD",
        "CCPP",
        "CCDI",
        "NSEGM",
        "ID_PROD",
        "UA",
        "P1001A_TOTAL",
        "P1000_TOTAL",
        "P1001A_2A_1C",
        "P1001A_2A_2C",
        "P1001A_2B_1C",
        "P1001A_2B_2C",
    ]
    cap1000 = read_csv(cap1000_path, usecols=cap1000_cols, low_memory=False)
    cap1000 = normalize_columns(cap1000)
    cap1000 = cap1000.rename(
        columns={
            "ANIO": "anio",
            "CCDD": "ccdd",
            "CCPP": "ccpp",
            "CCDI": "ccdi",
            "NSEGM": "psu",
            "ID_PROD": "id_prod",
            "UA": "ua",
            "P1001A_TOTAL": "gasto_agricola_total",
            "P1000_TOTAL": "costo_total_agropecuario",
            "P1001A_2A_1C": "jornaleros_perm_h",
            "P1001A_2A_2C": "jornaleros_perm_m",
            "P1001A_2B_1C": "jornaleros_event_h",
            "P1001A_2B_2C": "jornaleros_event_m",
        }
    )
    cap1000 = coerce_keys(cap1000, ID_COLS)

    cap200e_cols = [
        "ANIO",
        "CCDD",
        "CCPP",
        "CCDI",
        "NSEGM",
        "ID_PROD",
        "UA",
        "P237_VAL",
        "P239",
        "P241",
    ]
    cap200e = read_csv(cap200e_path, usecols=cap200e_cols, low_memory=False)
    cap200e = normalize_columns(cap200e)
    cap200e = cap200e.rename(
        columns={
            "ANIO": "anio",
            "CCDD": "ccdd",
            "CCPP": "ccpp",
            "CCDI": "ccdi",
            "NSEGM": "psu",
            "ID_PROD": "id_prod",
            "UA": "ua",
            "P237_VAL": "gasto_abono",
            "P239": "gasto_fertilizantes",
            "P241": "gasto_plaguicidas",
        }
    )
    cap200e = coerce_keys(cap200e, ID_COLS)
    for col in ["gasto_abono", "gasto_fertilizantes", "gasto_plaguicidas"]:
        cap200e[col] = pd.to_numeric(cap200e[col], errors="coerce")
    cap200e_agg = (
        cap200e.groupby(ID_COLS, dropna=False)[["gasto_abono", "gasto_fertilizantes", "gasto_plaguicidas"]]
        .sum()
        .reset_index()
    )

    practice_cols = [
        "ANIO",
        "CCDD",
        "CCPP",
        "CCDI",
        "NSEGM",
        "ID_PROD",
        "UA",
        "P301A_1",
        "P301A_2",
        "P301A_3",
        "P301A_4",
        "P301A_4A",
        "P301A_4B",
        "P301A_4C",
        "P301A_5",
        "P301A_6",
        "P301A_7",
        "P301A_8",
        "P301A_9",
        "P301A_10",
        "P301A_11",
        "P301A_12",
        "P301A_12A",
        "P301A_12B",
        "P301A_12C",
        "P301A_13",
        "P301A_14",
        "P301A_15",
        "P301A_16",
        "P301A_17",
    ]
    cap300 = read_csv(cap300_path, usecols=practice_cols, low_memory=False)
    cap300 = normalize_columns(cap300)
    cap300 = cap300.rename(
        columns={
            "ANIO": "anio",
            "CCDD": "ccdd",
            "CCPP": "ccpp",
            "CCDI": "ccdi",
            "NSEGM": "psu",
            "ID_PROD": "id_prod",
            "UA": "ua",
        }
    )
    cap300 = coerce_keys(cap300, ID_COLS)
    practice_vars = [c for c in cap300.columns if c.startswith("P301A_")]
    for col in practice_vars:
        cap300[col] = pd.to_numeric(cap300[col], errors="coerce")
    cap300["num_practices"] = cap300[practice_vars].eq(1).sum(axis=1)
    cap300["practice_any"] = (cap300["num_practices"] > 0).astype(int)
    cap300 = cap300[ID_COLS + ["practice_any", "num_practices"]]

    model = (
        features.merge(cap1000, on=ID_COLS, how="left")
        .merge(cap200e_agg, on=ID_COLS, how="left")
        .merge(cap300, on=ID_COLS, how="left")
    )

    labor_cols = ["jornaleros_perm_h", "jornaleros_perm_m", "jornaleros_event_h", "jornaleros_event_m"]
    for col in labor_cols + ["gasto_agricola_total", "costo_total_agropecuario"]:
        if col in model.columns:
            model[col] = pd.to_numeric(model[col], errors="coerce")

    model["labor_total"] = model[labor_cols].sum(axis=1, skipna=True)
    model["input_costs"] = model[["gasto_abono", "gasto_fertilizantes", "gasto_plaguicidas"]].sum(axis=1, skipna=True)
    model["size_cat"] = pd.cut(
        model["area_total_ha"],
        bins=[-float("inf"), 2, 5, float("inf")],
        labels=["pequeno_<2ha", "mediano_2_5ha", "grande_>5ha"],
    )

    model_path = PROCESSED_DIR / "model_data_ena2024.parquet"
    model.to_parquet(model_path, index=False)

    csv_path = PROCESSED_DIR / "model_data_ena2024.csv"
    model.to_csv(csv_path, index=False)

    print(f"Wrote {model_path}")
    print(f"Wrote {csv_path}")
    print(f"Rows: {len(model)} | Cols: {model.shape[1]}")

    key_vars = [
        "valor_total",
        "area_total_ha",
        "labor_total",
        "input_costs",
        "diversificacion_area",
        "practice_any",
        "weight",
        "estrato",
        "psu",
    ]
    print("Model variables:", key_vars)
    missing = {var: float(model[var].isna().mean()) for var in key_vars if var in model.columns}
    print(f"Missing share: {missing}")

    checks = {
        "neg_valor_total": int((model["valor_total"] < 0).sum()),
        "neg_area_total_ha": int((model["area_total_ha"] < 0).sum()),
        "neg_input_costs": int((model["input_costs"] < 0).sum()),
    }
    print(f"Range checks: {checks}")


if __name__ == "__main__":
    sys.exit(main())
