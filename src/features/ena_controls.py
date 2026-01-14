#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from ena.io import normalize_columns, read_csv


REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "raw" / "ENA_2024"
INTERMEDIATE_DIR = REPO_ROOT / "data" / "intermediate"
MAP_PATH = INTERMEDIATE_DIR / "variable_map.json"

ID_COLS = ["anio", "ccdd", "ccpp", "ccdi", "psu", "id_prod", "ua"]


def load_variable_map() -> dict[str, str]:
    with MAP_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def coerce_keys(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    df = df.copy()
    for col in keys:
        if col in df.columns:
            series = df[col].astype("string")
            df[col] = series.str.replace(r"\.0$", "", regex=True)
    return df


def load_module(path: Path, raw_cols: list[str], variable_map: dict[str, str]) -> pd.DataFrame:
    df = read_csv(path, usecols=raw_cols, low_memory=False)
    df = normalize_columns(df)
    rename_map = {raw: variable_map.get(raw, raw) for raw in raw_cols}
    df = df.rename(columns=rename_map)
    return coerce_keys(df, ID_COLS)


def yes_no_dummy(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    return (numeric == 1).astype(int)


def irrigation_features() -> pd.DataFrame:
    variable_map = load_variable_map()
    schema_path = INTERMEDIATE_DIR / "ena2024_schema.parquet"
    schema_cols = ID_COLS + ["water_source", "irrigation_system"]
    schema = pd.read_parquet(schema_path, columns=schema_cols)
    schema = coerce_keys(schema, ID_COLS)

    water_source = pd.to_numeric(schema["water_source"], errors="coerce")
    irrigation_system = pd.to_numeric(schema["irrigation_system"], errors="coerce")

    schema["riego_crop"] = ((water_source.notna()) & (water_source != 1)).astype(int)
    schema["riego_tecnificado_crop"] = irrigation_system.isin([1, 2, 3, 4, 5, 6]).astype(int)

    crop_agg = (
        schema.groupby(ID_COLS, dropna=False)
        .agg(
            riego_any=("riego_crop", "max"),
            riego_share=("riego_crop", "mean"),
            riego_tecnificado_any=("riego_tecnificado_crop", "max"),
            riego_tecnificado_share=("riego_tecnificado_crop", "mean"),
        )
        .reset_index()
    )

    cap800_path = RAW_DIR / "973-Modulo1908" / "16_CAP800.csv"
    cap800_cols = ["ANIO", "CCDD", "CCPP", "CCDI", "NSEGM", "ID_PROD", "UA", "P810"]
    cap800 = load_module(cap800_path, cap800_cols, variable_map)
    cap800["usuario_agua"] = yes_no_dummy(cap800["usuario_agua"])
    cap800 = cap800[ID_COLS + ["usuario_agua"]].drop_duplicates(subset=ID_COLS)

    cap1000_path = RAW_DIR / "973-Modulo1910" / "18_CAP1000.csv"
    cap1000_cols = ["ANIO", "CCDD", "CCPP", "CCDI", "NSEGM", "ID_PROD", "UA", "P1001A_3"]
    cap1000 = load_module(cap1000_path, cap1000_cols, variable_map)
    cap1000["gasto_agua_riego"] = pd.to_numeric(cap1000["gasto_agua_riego"], errors="coerce").fillna(0)
    cap1000 = cap1000[ID_COLS + ["gasto_agua_riego"]].drop_duplicates(subset=ID_COLS)

    merged = crop_agg.merge(cap800, on=ID_COLS, how="left").merge(cap1000, on=ID_COLS, how="left")
    merged["usuario_agua"] = merged["usuario_agua"].fillna(0).astype(int)
    merged["gasto_agua_riego"] = merged["gasto_agua_riego"].fillna(0)

    return merged


def machinery_capital_features() -> pd.DataFrame:
    variable_map = load_variable_map()
    cap1000_path = RAW_DIR / "973-Modulo1910" / "18_CAP1000.csv"
    cap1000_cols = [
        "ANIO",
        "CCDD",
        "CCPP",
        "CCDI",
        "NSEGM",
        "ID_PROD",
        "UA",
        "P1206",
        "P1001A_5A",
        "P1001A_5B",
        "P1001A_6A",
    ]
    cap1000 = load_module(cap1000_path, cap1000_cols, variable_map)
    cap1000["uso_maquinaria"] = yes_no_dummy(cap1000["uso_maquinaria"])
    for col in ["gasto_compra_equipos", "gasto_compra_maquinaria", "gasto_alquiler_mant_equipos"]:
        cap1000[col] = pd.to_numeric(cap1000[col], errors="coerce").fillna(0)
    cap1000 = cap1000[
        ID_COLS
        + ["uso_maquinaria", "gasto_compra_equipos", "gasto_compra_maquinaria", "gasto_alquiler_mant_equipos"]
    ]

    cap1200_path = RAW_DIR / "973-Modulo1913" / "21_CAP1200B_ME.csv"
    cap1200_cols = ["ANIO", "CCDD", "CCPP", "CCDI", "NSEGM", "ID_PROD", "UA", "P1207_N"]
    cap1200 = load_module(cap1200_path, cap1200_cols, variable_map)
    cap1200["num_maquinaria_equipo"] = pd.to_numeric(cap1200["num_maquinaria_equipo"], errors="coerce").fillna(0)
    cap1200_agg = (
        cap1200.groupby(ID_COLS, dropna=False)["num_maquinaria_equipo"].sum().reset_index()
    )

    merged = cap1000.merge(cap1200_agg, on=ID_COLS, how="left")
    merged["num_maquinaria_equipo"] = merged["num_maquinaria_equipo"].fillna(0)

    return merged


def fertilizer_seed_features() -> pd.DataFrame:
    variable_map = load_variable_map()
    cap200e_path = RAW_DIR / "973-Modulo1899" / "07_CAP200E.csv"
    cap200e_cols = [
        "ANIO",
        "CCDD",
        "CCPP",
        "CCDI",
        "NSEGM",
        "ID_PROD",
        "UA",
        "P235_VAL",
        "P235A_4",
        "P235A_9",
        "P236",
        "P238",
    ]
    cap200e = load_module(cap200e_path, cap200e_cols, variable_map)
    cap200e["gasto_semilla"] = pd.to_numeric(cap200e["gasto_semilla"], errors="coerce").fillna(0)
    cap200e["semilla_semillero"] = pd.to_numeric(cap200e["semilla_semillero"], errors="coerce").fillna(0)
    cap200e["semilla_comercial"] = pd.to_numeric(cap200e["semilla_comercial"], errors="coerce").fillna(0)
    cap200e["usa_abono"] = yes_no_dummy(cap200e["usa_abono"])
    cap200e["usa_fertilizantes"] = yes_no_dummy(cap200e["usa_fertilizantes"])

    cap200e_agg = (
        cap200e.groupby(ID_COLS, dropna=False)
        .agg(
            gasto_semilla=("gasto_semilla", "sum"),
            usa_abono=("usa_abono", "max"),
            usa_fertilizantes=("usa_fertilizantes", "max"),
            semilla_semillero_any=("semilla_semillero", "max"),
            semilla_comercial_any=("semilla_comercial", "max"),
        )
        .reset_index()
    )

    schema_path = INTERMEDIATE_DIR / "ena2024_schema.parquet"
    schema_cols = ID_COLS + ["seed_certified"]
    schema = pd.read_parquet(schema_path, columns=schema_cols)
    schema = coerce_keys(schema, ID_COLS)
    seed_code = pd.to_numeric(schema["seed_certified"], errors="coerce")
    schema["semilla_certificada_crop"] = pd.Series(index=schema.index, dtype="float")
    schema.loc[seed_code == 1, "semilla_certificada_crop"] = 1
    schema.loc[seed_code == 2, "semilla_certificada_crop"] = 0

    seed_agg = (
        schema.groupby(ID_COLS, dropna=False)
        .agg(
            semilla_certificada_any=("semilla_certificada_crop", "max"),
            semilla_certificada_share=("semilla_certificada_crop", "mean"),
        )
        .reset_index()
    )
    seed_agg["semilla_certificada_any"] = seed_agg["semilla_certificada_any"].fillna(0)
    seed_agg["semilla_certificada_share"] = seed_agg["semilla_certificada_share"].fillna(0)

    merged = cap200e_agg.merge(seed_agg, on=ID_COLS, how="left")

    return merged


def extension_credit_education_features() -> pd.DataFrame:
    variable_map = load_variable_map()

    cap700_path = RAW_DIR / "973-Modulo1907" / "15_CAP700.csv"
    cap700_cols = ["ANIO", "CCDD", "CCPP", "CCDI", "NSEGM", "ID_PROD", "UA", "P701", "P704"]
    cap700 = load_module(cap700_path, cap700_cols, variable_map)
    cap700["capacitacion_recibida"] = yes_no_dummy(cap700["capacitacion_recibida"])
    cap700["asistencia_tecnica_recibida"] = yes_no_dummy(cap700["asistencia_tecnica_recibida"])
    cap700 = cap700[ID_COLS + ["capacitacion_recibida", "asistencia_tecnica_recibida"]].drop_duplicates(
        subset=ID_COLS
    )

    cap900_path = RAW_DIR / "973-Modulo1909" / "17_CAP900.csv"
    cap900_cols = ["ANIO", "CCDD", "CCPP", "CCDI", "NSEGM", "ID_PROD", "UA", "P902"]
    cap900 = load_module(cap900_path, cap900_cols, variable_map)
    cap900["credito_obtenido"] = yes_no_dummy(cap900["credito_obtenido"])
    cap900 = cap900[ID_COLS + ["credito_obtenido"]].drop_duplicates(subset=ID_COLS)

    cap1100_path = RAW_DIR / "973-Modulo1911" / "19_CAP1100.csv"
    cap1100_cols = ["ANIO", "CCDD", "CCPP", "CCDI", "NSEGM", "ID_PROD", "UA", "P1105"]
    cap1100 = load_module(cap1100_path, cap1100_cols, variable_map)
    cap1100["nivel_educacion"] = pd.to_numeric(cap1100["nivel_educacion"], errors="coerce")
    educ_median = cap1100["nivel_educacion"].median()
    cap1100["nivel_educacion"] = cap1100["nivel_educacion"].fillna(educ_median)
    cap1100 = cap1100[ID_COLS + ["nivel_educacion"]].drop_duplicates(subset=ID_COLS)

    cap800_path = RAW_DIR / "973-Modulo1908" / "16_CAP800.csv"
    cap800_cols = ["ANIO", "CCDD", "CCPP", "CCDI", "NSEGM", "ID_PROD", "UA", "P801", "P801_1"]
    cap800 = load_module(cap800_path, cap800_cols, variable_map)
    cap800["asociacion_miembro"] = yes_no_dummy(cap800["asociacion_miembro"])
    cap800["asociacion_num"] = pd.to_numeric(cap800["asociacion_num"], errors="coerce").fillna(0)
    cap800 = cap800[ID_COLS + ["asociacion_miembro", "asociacion_num"]].drop_duplicates(subset=ID_COLS)

    merged = cap700.merge(cap900, on=ID_COLS, how="left")
    merged = merged.merge(cap1100, on=ID_COLS, how="left")
    merged = merged.merge(cap800, on=ID_COLS, how="left")

    for col in ["capacitacion_recibida", "asistencia_tecnica_recibida", "credito_obtenido", "asociacion_miembro"]:
        merged[col] = merged[col].fillna(0).astype(int)
    merged["asociacion_num"] = merged["asociacion_num"].fillna(0)

    return merged
