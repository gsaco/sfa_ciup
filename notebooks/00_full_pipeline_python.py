# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
#   kernelspec:
#     display_name: Python 3 (sfa_ciup)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 00 - Full ENA 2024 Python Pipeline (Cleaning to Modeling Data)
#
# This notebook is a long, end-to-end, **Python-only** reconstruction of the
# ENA 2024 data pipeline. It expands the existing scripts into a readable,
# step-by-step workflow that:
#
# 1. Profiles raw modules and checks key integrity.
# 2. Parses the official PDF dictionary and standardizes variable names.
# 3. Builds the long, crop-level schema dataset.
# 4. Computes diversification indices (HHI, Shannon) at the producer level.
# 5. Merges costs, labor, and practices into the modeling dataset.
# 6. Builds the expanded controls dataset (irrigation, machinery, seed, credit).
# 7. Merges external geo and climate features (when available).
#
# The notebook minimizes external dependencies by embedding the core logic
# directly, while still saving outputs to the same folders as the pipeline
# scripts (`data/intermediate`, `data/processed`, `outputs/tables`).
#
# **Note:** This is the Python pipeline only. The R steps are intentionally
# excluded.

# %% [markdown]
# ## 0. Setup
#
# Configure paths, display options, and caching behavior. Toggle `USE_CACHED`
# or `FORCE_REBUILD` to control recomputation.

# %%
from __future__ import annotations

from pathlib import Path
import json
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# %%
USE_CACHED = True
FORCE_REBUILD = False
SAVE_PLOTS = False


def find_repo_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    for parent in [start] + list(start.parents):
        if (parent / "src").exists() and (parent / "data").exists():
            return parent
    raise RuntimeError("Could not locate repo root. Run from within the repo.")


REPO_ROOT = find_repo_root()
RAW_DIR = REPO_ROOT / "data" / "raw" / "ENA_2024"
INTERMEDIATE_DIR = REPO_ROOT / "data" / "intermediate"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
EXTERNAL_DIR = REPO_ROOT / "data" / "external" / "processed"
OUTPUT_TABLES = REPO_ROOT / "outputs" / "tables"
DOCS_DIR = REPO_ROOT / "docs"

DICT_PATH = REPO_ROOT / "DICCIONARIO DE DATOS ENA-2024.pdf"

pd.set_option("display.max_columns", 200)

sns.set_theme(style="whitegrid")

# %% [markdown]
# ### Helper utilities
#
# Lightweight IO and helper functions are inlined here to keep the notebook
# readable and self-contained.

# %%
DEFAULT_ENCODINGS = ("utf-8", "latin-1", "cp1252")


def read_csv(path: str | Path, **kwargs: object) -> pd.DataFrame:
    last_err: Exception | None = None
    for enc in DEFAULT_ENCODINGS:
        try:
            return pd.read_csv(path, encoding=enc, **kwargs)
        except UnicodeDecodeError as err:
            last_err = err
    if last_err is not None:
        raise last_err
    return pd.read_csv(path, **kwargs)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    return df


def coerce_keys(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    df = df.copy()
    for col in keys:
        if col in df.columns:
            series = df[col].astype("string")
            df[col] = series.str.replace(r"\.0$", "", regex=True)
    return df


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def outputs_exist(paths: list[Path]) -> bool:
    return all(p.exists() for p in paths)


def maybe_use_cache(paths: list[Path]) -> bool:
    return USE_CACHED and not FORCE_REBUILD and outputs_exist(paths)


def to_markdown(df: pd.DataFrame) -> str:
    try:
        return df.to_markdown(index=False)
    except Exception:
        cols = df.columns.tolist()
        lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
        for _, row in df.iterrows():
            lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
        return "\n".join(lines)


# %% [markdown]
# ## 1. Raw data availability and quick inventory
#
# We first confirm that the ENA raw files are present and summarize how many
# CSV files are available.

# %%
if not RAW_DIR.exists():
    raise FileNotFoundError(f"Missing raw data folder: {RAW_DIR}")

csv_paths = list(RAW_DIR.rglob("*.csv"))
print(f"Raw ENA CSV files found: {len(csv_paths)}")

# %% [markdown]
# ## 2. Module profiling (keys, missingness, duplicates)
#
# This replicates the logic in `src/ena/01_load_and_profile.py`. We profile
# each module, track key completeness, and store a standardized `CARATULA`
# dataset for later joins.

# %%
KEY_COLS = ["ANIO", "CCDD", "CCPP", "CCDI", "NSEGM", "ID_PROD", "UA"]
DESIGN_COLS = ["ESTRATO", "FACTOR_PRODUCTOR", "FACTOR_SUPERFICIE", "NSEGM"]
POTENTIAL_CROP_ID_COLS = [
    "P115_COD",
    "P204_COD",
    "P229C_COD",
    "P229G_COD",
    "P234_COD",
    "P419_COD",
    "P1202_COD",
    "P1207_COD",
]


def profile_file(path: Path) -> dict[str, object]:
    header = read_csv(path, nrows=0)
    header = normalize_columns(header)
    cols = header.columns.tolist()

    key_cols = [c for c in KEY_COLS if c in cols]
    crop_id_cols = [c for c in POTENTIAL_CROP_ID_COLS if c in cols]
    design_cols = [c for c in DESIGN_COLS if c in cols]
    usecols = sorted(set(key_cols + crop_id_cols))

    df = read_csv(path, usecols=usecols if usecols else None, low_memory=False)
    df = normalize_columns(df)

    nrows = len(df)
    ncols = len(cols)
    missing = {col: float(df[col].isna().mean()) for col in key_cols}

    dup_keys = None
    if key_cols:
        dup_keys = int(df.duplicated(subset=key_cols).sum())

    dup_keys_crop = None
    crop_id = crop_id_cols[0] if crop_id_cols else ""
    if key_cols and crop_id:
        dup_keys_crop = int(df.duplicated(subset=key_cols + [crop_id]).sum())

    return {
        "file": path.relative_to(REPO_ROOT).as_posix(),
        "rows": nrows,
        "cols": ncols,
        "key_cols": ",".join(key_cols),
        "design_cols": ",".join(design_cols),
        "missing_keys": ";".join(f"{k}:{missing[k]:.4f}" for k in key_cols),
        "dup_keys": dup_keys,
        "crop_id_col": crop_id,
        "dup_keys_crop": dup_keys_crop,
    }


profile_outputs = [INTERMEDIATE_DIR / "module_profile.csv", INTERMEDIATE_DIR / "ena2024_raw.parquet"]

if maybe_use_cache(profile_outputs):
    module_profile = pd.read_csv(INTERMEDIATE_DIR / "module_profile.csv")
    caratula = pd.read_parquet(INTERMEDIATE_DIR / "ena2024_raw.parquet")
    print("[cache] module profiling: using existing outputs")
else:
    ensure_dir(INTERMEDIATE_DIR)

    profiles = [profile_file(path) for path in csv_paths]
    module_profile = pd.DataFrame(profiles)
    module_profile.to_csv(INTERMEDIATE_DIR / "module_profile.csv", index=False)

    caratula_path = RAW_DIR / "973-Modulo1893" / "CARATULA.csv"
    if not caratula_path.exists():
        raise FileNotFoundError(f"Expected CARATULA at {caratula_path}")
    caratula = read_csv(caratula_path, low_memory=False)
    caratula = normalize_columns(caratula)
    caratula.to_parquet(INTERMEDIATE_DIR / "ena2024_raw.parquet", index=False)

    print("Wrote module_profile.csv and ena2024_raw.parquet")

module_profile.head(10)

# %% [markdown]
# ### Module profile summary
#
# We check the distribution of missingness in key variables across modules.

# %%
missing_summary = (
    module_profile.assign(missing_key_share=module_profile["missing_keys"].str.extract(r"ANIO:(\d\.\d+)")[0])
    .assign(missing_key_share=lambda df: pd.to_numeric(df["missing_key_share"], errors="coerce"))
    .sort_values("missing_key_share", ascending=False)
)
missing_summary.head(10)

# %%
plt.figure(figsize=(8, 4))
plot_df = missing_summary.dropna(subset=["missing_key_share"]).head(15)
plt.barh(plot_df["file"], plot_df["missing_key_share"])
plt.xlabel("Missing share for ANIO (proxy)")
plt.title("Modules with highest missingness in ANIO")
plt.tight_layout()
if SAVE_PLOTS:
    plt.savefig(OUTPUT_TABLES / "profile_missing_anio.png", dpi=200)
plt.show()

# %% [markdown]
# ## 3. Build the standardized schema from the PDF dictionary
#
# This step parses the official PDF dictionary and creates:
# - `data/intermediate/ena2024_dictionary.csv`
# - `data/intermediate/variable_map.json`
# - `docs/ENA2024_VARIABLE_DICTIONARY.md`
#
# The variable map is then used to rename raw ENA variables into a clean
# standardized schema.

# %%
import pdfplumber
import re


def normalize_text(text: str) -> str:
    return " ".join(text.replace("\n", " ").split())


def normalize_var(text: str) -> str:
    cleaned = text.replace("\n", "").replace(" ", "")
    cleaned = cleaned.replace("-", "")
    return cleaned.strip()


def infer_unit(description: str) -> str:
    desc = description.lower()
    if "hect" in desc:
        return "ha"
    if re.search(r"\bS/|\bSoles\b", description, flags=re.IGNORECASE):
        return "S/"
    if "kilogram" in desc or "kg" in desc:
        return "kg"
    if "anio" in desc or "a\xF1o" in desc:
        return "year"
    return ""


def extract_dictionary(pdf_path: Path) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables() or []
            for table in tables:
                if not table or len(table) < 2:
                    continue
                for row in table[1:]:
                    if not row or len(row) < 3:
                        continue
                    var = normalize_var((row[1] or "").strip())
                    desc = (row[2] or "").strip()
                    if not var:
                        continue
                    rows.append(
                        {
                            "variable": var,
                            "description": normalize_text(desc),
                            "type": (row[4] or "").strip() if len(row) > 4 else "",
                            "length": (row[5] or "").strip() if len(row) > 5 else "",
                            "decimal": (row[6] or "").strip() if len(row) > 6 else "",
                            "page": page_idx,
                        }
                    )
    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("No dictionary entries extracted from PDF.")
    df = df.drop_duplicates(subset=["variable"], keep="first").reset_index(drop=True)
    return df


def build_schema_map() -> list[dict[str, str]]:
    return [
        {"raw": "ANIO", "std": "anio", "notes": "Survey year."},
        {"raw": "CCDD", "std": "ccdd", "notes": "Department code."},
        {"raw": "NOMBREDD", "std": "departamento", "notes": "Department name."},
        {"raw": "CCPP", "std": "ccpp", "notes": "Province code."},
        {"raw": "NOMBREPV", "std": "provincia", "notes": "Province name."},
        {"raw": "CCDI", "std": "ccdi", "notes": "District code."},
        {"raw": "NOMBREDI", "std": "distrito", "notes": "District name."},
        {"raw": "NSEGM", "std": "psu", "notes": "Primary sampling unit (segment)."},
        {"raw": "ID_PROD", "std": "id_prod", "notes": "Producer identifier."},
        {"raw": "UA", "std": "ua", "notes": "Agricultural unit."},
        {"raw": "REGION", "std": "region_natural", "notes": "Natural region."},
        {"raw": "ESTRATO", "std": "estrato", "notes": "Sampling stratum."},
        {"raw": "FACTOR_PRODUCTOR", "std": "weight", "notes": "Expansion weight for producer."},
        {"raw": "LATITUD", "std": "latitud", "notes": "Latitude."},
        {"raw": "LONGITUD", "std": "longitud", "notes": "Longitude."},
        {"raw": "P204_COD", "std": "crop_code", "notes": "Crop code."},
        {"raw": "P204_NOM", "std": "crop_name", "notes": "Crop name."},
        {"raw": "P217_SUP_ha", "std": "area_cosechada_ha", "notes": "Harvested area by crop."},
        {"raw": "P219_CANT_1", "std": "produccion_cant_ent", "notes": "Production quantity (integer)."},
        {"raw": "P219_CANT_2", "std": "produccion_cant_dec", "notes": "Production quantity (decimal)."},
        {"raw": "P220_1_VAL", "std": "valor_venta", "notes": "Value sold."},
        {"raw": "P220_2_VAL", "std": "valor_consumo", "notes": "Value for household consumption."},
        {"raw": "P220_3A_VAL", "std": "valor_semilla_autoconsumo", "notes": "Value for seed (auto-consumption)."},
        {"raw": "P220_3B_VAL", "std": "valor_semilla_venta", "notes": "Value for seed (sold)."},
        {"raw": "P1001A_TOTAL", "std": "gasto_agricola_total", "notes": "Total agricultural expenses."},
        {"raw": "P1000_TOTAL", "std": "costo_total_agropecuario", "notes": "Total agricultural + livestock cost."},
        {"raw": "P1001A_2A_1C", "std": "jornaleros_perm_h", "notes": "Permanent workers (men)."},
        {"raw": "P1001A_2A_2C", "std": "jornaleros_perm_m", "notes": "Permanent workers (women)."},
        {"raw": "P1001A_2B_1C", "std": "jornaleros_event_h", "notes": "Seasonal workers (men)."},
        {"raw": "P1001A_2B_2C", "std": "jornaleros_event_m", "notes": "Seasonal workers (women)."},
        {"raw": "P237_VAL", "std": "gasto_abono", "notes": "Expenditure on organic fertilizer."},
        {"raw": "P239", "std": "gasto_fertilizantes", "notes": "Expenditure on fertilizers."},
        {"raw": "P241", "std": "gasto_plaguicidas", "notes": "Expenditure on pesticides."},
        {"raw": "P301A_1", "std": "practica_analisis_suelos", "notes": "Agricultural practice."},
        {"raw": "P301A_2", "std": "practica_materia_organica", "notes": "Agricultural practice."},
        {"raw": "P301A_3", "std": "practica_rotacion_cultivos", "notes": "Agricultural practice."},
        {"raw": "P301A_4", "std": "practica_terrazas_zanjas", "notes": "Agricultural practice."},
        {"raw": "P301A_4A", "std": "practica_recuperacion_erosion", "notes": "Agricultural practice."},
        {"raw": "P301A_4B", "std": "practica_recuperacion_compactacion", "notes": "Agricultural practice."},
        {"raw": "P301A_4C", "std": "practica_recuperacion_salinos", "notes": "Agricultural practice."},
        {"raw": "P301A_5", "std": "practica_arar_tierra", "notes": "Agricultural practice."},
        {"raw": "P301A_6", "std": "practica_desterronar", "notes": "Agricultural practice."},
        {"raw": "P301A_7", "std": "practica_nivelar_terreno", "notes": "Agricultural practice."},
        {"raw": "P301A_8", "std": "practica_surcos_contorno", "notes": "Agricultural practice."},
        {"raw": "P301A_9", "std": "practica_agua_necesaria", "notes": "Agricultural practice."},
        {"raw": "P301A_10", "std": "practica_frecuencia_riego", "notes": "Agricultural practice."},
        {"raw": "P301A_11", "std": "practica_medir_agua", "notes": "Agricultural practice."},
        {"raw": "P301A_12", "std": "practica_mantenimiento_riego", "notes": "Agricultural practice."},
        {"raw": "P301A_12A", "std": "practica_analisis_agua", "notes": "Agricultural practice."},
        {"raw": "P301A_12B", "std": "practica_construccion_diques", "notes": "Agricultural practice."},
        {"raw": "P301A_12C", "std": "practica_waru_waru", "notes": "Agricultural practice."},
        {"raw": "P301A_13", "std": "practica_usar_abonos", "notes": "Agricultural practice."},
        {"raw": "P301A_14", "std": "practica_usar_fertilizantes", "notes": "Agricultural practice."},
        {"raw": "P301A_15", "std": "practica_usar_plaguicidas", "notes": "Agricultural practice."},
        {"raw": "P301A_16", "std": "practica_control_biologico", "notes": "Agricultural practice."},
        {"raw": "P301A_17", "std": "practica_manejo_integrado_plagas", "notes": "Agricultural practice."},
        {"raw": "P212", "std": "water_source", "notes": "Water source for irrigation (crop-level)."},
        {"raw": "P213", "std": "irrigation_system", "notes": "Irrigation system used (crop-level)."},
        {"raw": "P214", "std": "seed_certified", "notes": "Certified seed indicator (crop-level)."},
        {"raw": "P235_VAL", "std": "gasto_semilla", "notes": "Seed expenditure (crop-level)."},
        {"raw": "P235A_4", "std": "semilla_semillero", "notes": "Seed source: semillero (crop-level)."},
        {"raw": "P235A_9", "std": "semilla_comercial", "notes": "Seed source: commercial establishment (crop-level)."},
        {"raw": "P236", "std": "usa_abono", "notes": "Used organic fertilizer (crop-level)."},
        {"raw": "P238", "std": "usa_fertilizantes", "notes": "Used fertilizers (crop-level)."},
        {"raw": "P1001A_3", "std": "gasto_agua_riego", "notes": "Irrigation water expenditure (agri)."},
        {"raw": "P1001A_4", "std": "gasto_asistencia_agricola", "notes": "Agricultural technical assistance expenditure."},
        {"raw": "P1001A_5A", "std": "gasto_compra_equipos", "notes": "Equipment purchase expenditure (agri)."},
        {"raw": "P1001A_5B", "std": "gasto_compra_maquinaria", "notes": "Machinery purchase expenditure (agri)."},
        {"raw": "P1001A_6A", "std": "gasto_alquiler_mant_equipos", "notes": "Equipment rental/maintenance expenditure (agri)."},
        {"raw": "P1206", "std": "uso_maquinaria", "notes": "Used machinery/equipment (agri)."},
        {"raw": "P1207_N", "std": "num_maquinaria_equipo", "notes": "Number of machinery/equipment items."},
        {"raw": "P1207_TIPO", "std": "tipo_maquinaria_equipo", "notes": "Machinery/equipment type."},
        {"raw": "P701", "std": "capacitacion_recibida", "notes": "Training received (last 3 years)."},
        {"raw": "P704", "std": "asistencia_tecnica_recibida", "notes": "Technical assistance received (last 3 years)."},
        {"raw": "P901", "std": "credito_solicitado", "notes": "Requested credit (last 12 months)."},
        {"raw": "P902", "std": "credito_obtenido", "notes": "Obtained credit (last 12 months)."},
        {"raw": "P1105", "std": "nivel_educacion", "notes": "Educational attainment level."},
        {"raw": "P801", "std": "asociacion_miembro", "notes": "Member of association/cooperative."},
        {"raw": "P801_1", "std": "asociacion_num", "notes": "Number of associations."},
        {"raw": "P810", "std": "usuario_agua", "notes": "Water user committee membership."},
    ]


schema_outputs = [
    INTERMEDIATE_DIR / "ena2024_dictionary.csv",
    INTERMEDIATE_DIR / "variable_map.json",
    DOCS_DIR / "ENA2024_VARIABLE_DICTIONARY.md",
]

if maybe_use_cache(schema_outputs):
    dict_df = pd.read_csv(INTERMEDIATE_DIR / "ena2024_dictionary.csv")
    with (INTERMEDIATE_DIR / "variable_map.json").open("r", encoding="utf-8") as handle:
        variable_map = json.load(handle)
    print("[cache] dictionary parsing: using existing outputs")
else:
    if not DICT_PATH.exists():
        raise FileNotFoundError(f"Dictionary not found: {DICT_PATH}")

    ensure_dir(INTERMEDIATE_DIR)
    ensure_dir(DOCS_DIR)

    dict_df = extract_dictionary(DICT_PATH)
    dict_df.to_csv(INTERMEDIATE_DIR / "ena2024_dictionary.csv", index=False)

    schema_map = build_schema_map()
    dict_lookup = dict(zip(dict_df["variable"], dict_df["description"]))

    table_rows: list[dict[str, str]] = []
    for item in schema_map:
        raw = item["raw"]
        std = item["std"]
        description = dict_lookup.get(raw, "")
        unit = infer_unit(description) if description else ""
        notes = item.get("notes", "")
        table_rows.append(
            {
                "raw_variable": raw,
                "standard_name": std,
                "definition": description,
                "unit": unit,
                "notes": notes,
            }
        )

    dictionary_md = DOCS_DIR / "ENA2024_VARIABLE_DICTIONARY.md"
    with dictionary_md.open("w", encoding="utf-8") as handle:
        handle.write("# ENA 2024 Variable Dictionary (Mapped)\n\n")
        handle.write("- Generated by notebook\n")
        handle.write(f"- Source: `{DICT_PATH}`\n\n")
        handle.write("| Variable original | Nombre estandarizado | Definicion | Unidad | Notas |\n")
        handle.write("|---|---|---|---|---|\n")
        for row in table_rows:
            handle.write(
                f"| {row['raw_variable']} | {row['standard_name']} | {row['definition']} | {row['unit']} | {row['notes']} |\n"
            )

    variable_map = {item["raw"]: item["std"] for item in schema_map}
    with (INTERMEDIATE_DIR / "variable_map.json").open("w", encoding="utf-8") as handle:
        json.dump(variable_map, handle, indent=2, ensure_ascii=True)

    print("Wrote ena2024_dictionary.csv, variable_map.json, and ENA2024_VARIABLE_DICTIONARY.md")

schema_map_df = pd.DataFrame(build_schema_map())
schema_map_df.head(10)

# %% [markdown]
# ### Dictionary coverage check
#
# Which variables in our schema map are present in the official dictionary?

# %%
coverage = schema_map_df.merge(dict_df, left_on="raw", right_on="variable", how="left")
coverage["in_dictionary"] = coverage["description"].notna()
coverage["in_dictionary"].mean()

# %% [markdown]
# ## 4. Apply schema to crop and household modules
#
# We merge the crop module with the cover module (`CARATULA`) to produce the
# long-format schema dataset with standardized variable names.

# %%
SCHEMA_OUTPUT = INTERMEDIATE_DIR / "ena2024_schema.parquet"

if maybe_use_cache([SCHEMA_OUTPUT]):
    schema_df = pd.read_parquet(SCHEMA_OUTPUT)
    print("[cache] apply schema: using existing output")
else:
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

    schema_df = crop.merge(caratula, on=KEY_COLS, how="left", validate="many_to_one")
    schema_df = schema_df.rename(columns=variable_map)

    ensure_dir(INTERMEDIATE_DIR)
    schema_df.to_parquet(SCHEMA_OUTPUT, index=False)
    print(f"Wrote {SCHEMA_OUTPUT}")

schema_df.head()

# %% [markdown]
# ### Schema integrity checks

# %%
missing_keys = {
    col: float(schema_df[col].isna().mean())
    for col in ["anio", "ccdd", "ccpp", "ccdi", "psu", "id_prod", "ua"]
    if col in schema_df.columns
}
missing_keys

# %% [markdown]
# ## 5. Compute diversification indices
#
# We compute diversification at the producer level using crop area and crop
# value. This produces the `ena2024_features.parquet` dataset used for modeling.

# %%
ID_COLS = ["anio", "ccdd", "ccpp", "ccdi", "psu", "id_prod", "ua"]


def compute_diversification(
    df: pd.DataFrame,
    id_cols: list[str],
    value_col: str,
    crop_col: str,
) -> pd.DataFrame:
    data = df[id_cols + [value_col, crop_col]].copy()
    data[value_col] = pd.to_numeric(data[value_col], errors="coerce")

    totals = data.groupby(id_cols)[value_col].transform("sum")
    data = data[totals > 0].copy()
    if data.empty:
        return pd.DataFrame(columns=id_cols + ["hhi", "diversificacion", "shannon", "num_crops", "total_value"])

    data["share"] = data[value_col] / totals[totals > 0]
    data = data[data["share"] > 0]

    grouped = data.groupby(id_cols, dropna=False)
    hhi = grouped["share"].apply(lambda x: float((x**2).sum()))
    shannon = grouped["share"].apply(lambda x: float(-(x * np.log(x)).sum()))
    num_crops = grouped[crop_col].nunique()
    total_value = grouped[value_col].sum()

    out = pd.DataFrame(
        {
            "hhi": hhi,
            "diversificacion": 1 - hhi,
            "shannon": shannon,
            "num_crops": num_crops,
            "total_value": total_value,
        }
    ).reset_index()
    return out


FEATURES_OUTPUT = PROCESSED_DIR / "ena2024_features.parquet"

if maybe_use_cache([FEATURES_OUTPUT]):
    features = pd.read_parquet(FEATURES_OUTPUT)
    print("[cache] diversification: using existing output")
else:
    ensure_dir(PROCESSED_DIR)
    ensure_dir(OUTPUT_TABLES)

    df = schema_df.copy()
    value_cols = [
        "valor_venta",
        "valor_consumo",
        "valor_semilla_autoconsumo",
        "valor_semilla_venta",
    ]
    for col in value_cols + ["area_cosechada_ha"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["valor_total_cultivo"] = df[value_cols].sum(axis=1, min_count=1)

    area_div = compute_diversification(
        df=df,
        id_cols=ID_COLS,
        value_col="area_cosechada_ha",
        crop_col="crop_code",
    ).rename(
        columns={
            "hhi": "hhi_area",
            "diversificacion": "diversificacion_area",
            "shannon": "shannon_area",
            "num_crops": "num_crops_area",
            "total_value": "area_total_ha",
        }
    )

    value_div = compute_diversification(
        df=df,
        id_cols=ID_COLS,
        value_col="valor_total_cultivo",
        crop_col="crop_code",
    ).rename(
        columns={
            "hhi": "hhi_valor",
            "diversificacion": "diversificacion_valor",
            "shannon": "shannon_valor",
            "num_crops": "num_crops_valor",
            "total_value": "valor_total",
        }
    )

    base_cols = ID_COLS + [
        "region_natural",
        "estrato",
        "weight",
        "departamento",
        "provincia",
        "distrito",
        "latitud",
        "longitud",
    ]
    base = df[base_cols].drop_duplicates(subset=ID_COLS)

    features = base.merge(area_div, on=ID_COLS, how="left").merge(value_div, on=ID_COLS, how="left")

    features.to_parquet(FEATURES_OUTPUT, index=False)

    features["size_cat"] = pd.cut(
        features["area_total_ha"],
        bins=[-float("inf"), 2, 5, float("inf")],
        labels=["pequeno_<2ha", "mediano_2_5ha", "grande_>5ha"],
    )

    summary_frames = []
    overall = features.assign(group_type="overall", group="overall")
    summary_frames.append(overall)

    if "region_natural" in features.columns:
        summary_frames.append(features.assign(group_type="region", group=features["region_natural"]))
    summary_frames.append(features.assign(group_type="size", group=features["size_cat"].astype("string")))

    summary = (
        pd.concat(summary_frames, ignore_index=True)
        .groupby(["group_type", "group"], dropna=False)
        .agg(
            n=("id_prod", "count"),
            mean_diversificacion=("diversificacion_area", "mean"),
            mean_hhi=("hhi_area", "mean"),
            mean_num_crops=("num_crops_area", "mean"),
            mean_area_ha=("area_total_ha", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(OUTPUT_TABLES / "01_diversification_descriptives.csv", index=False)
    (OUTPUT_TABLES / "01_diversification_descriptives.md").write_text(to_markdown(summary), encoding="utf-8")

    print("Wrote ena2024_features.parquet and diversification summary tables")

features.head()

# %% [markdown]
# ### Diversification plots
#
# We visualize key diversification metrics and farm size distributions.

# %%
plt.figure(figsize=(6, 4))
sns.histplot(features["diversificacion_area"].dropna(), bins=40)
plt.title("Diversificacion (area) distribution")
plt.tight_layout()
if SAVE_PLOTS:
    plt.savefig(OUTPUT_TABLES / "diversificacion_area_hist.png", dpi=200)
plt.show()

# %%
plt.figure(figsize=(6, 4))
sns.histplot(np.log1p(features["area_total_ha"].dropna()), bins=40)
plt.title("log(1 + area_total_ha)")
plt.tight_layout()
if SAVE_PLOTS:
    plt.savefig(OUTPUT_TABLES / "area_total_log_hist.png", dpi=200)
plt.show()

# %% [markdown]
# ## 6. Build the core model dataset (costs, labor, practices)
#
# This step merges diversification features with cost, labor, and practice data
# from multiple ENA modules.

# %%
PRACTICE_ANY_VARS = [
    "P301A_1",
    "P301A_2",
    "P301A_3",
    "P301A_4",
    "P301A_4A",
    "P301A_4B",
    "P301A_4C",
    "P301A_11",
    "P301A_16",
    "P301A_17",
]


def sum_components(df: pd.DataFrame, components: list[str]) -> pd.Series:
    if not components:
        return pd.Series([pd.NA] * len(df), index=df.index, dtype="float")
    return df[components].sum(axis=1, min_count=1)


def component_missingness(df: pd.DataFrame, components: list[str]) -> dict[str, float | int]:
    if not components:
        return {
            "n_rows": len(df),
            "n_all_missing": 0,
            "n_partial_missing": 0,
            "all_missing_share": float("nan"),
            "partial_missing_share": float("nan"),
            "any_missing_share": float("nan"),
        }

    subset = df[components]
    all_missing = subset.isna().all(axis=1)
    any_missing = subset.isna().any(axis=1)
    partial_missing = any_missing & ~all_missing
    return {
        "n_rows": int(len(subset)),
        "n_all_missing": int(all_missing.sum()),
        "n_partial_missing": int(partial_missing.sum()),
        "all_missing_share": float(all_missing.mean()) if len(subset) else float("nan"),
        "partial_missing_share": float(partial_missing.mean()) if len(subset) else float("nan"),
        "any_missing_share": float(any_missing.mean()) if len(subset) else float("nan"),
    }


MODEL_OUTPUT = PROCESSED_DIR / "model_data_ena2024.parquet"
MODEL_CSV = PROCESSED_DIR / "model_data_ena2024.csv"

if maybe_use_cache([MODEL_OUTPUT, MODEL_CSV]):
    model = pd.read_parquet(MODEL_OUTPUT)
    print("[cache] model data: using existing outputs")
else:
    ensure_dir(PROCESSED_DIR)
    ensure_dir(OUTPUT_TABLES)

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
        .sum(min_count=1)
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
        *PRACTICE_ANY_VARS,
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

    missing_practice_vars = [col for col in PRACTICE_ANY_VARS if col not in cap300.columns]
    if missing_practice_vars:
        raise ValueError(f"Missing practice variables in CAP300: {missing_practice_vars}")

    for col in PRACTICE_ANY_VARS:
        cap300[col] = pd.to_numeric(cap300[col], errors="coerce")
    practice_matrix = cap300[PRACTICE_ANY_VARS]
    practice_missingness = component_missingness(cap300, PRACTICE_ANY_VARS)
    num_practices = practice_matrix.eq(1).sum(axis=1, min_count=1)
    practice_any = num_practices.gt(0).where(num_practices.notna())
    cap300["num_practices"] = num_practices
    cap300["practice_any"] = practice_any.astype("Int64")
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

    model["labor_total"] = sum_components(model, labor_cols)
    model["input_costs"] = sum_components(model, ["gasto_abono", "gasto_fertilizantes", "gasto_plaguicidas"])
    model["size_cat"] = pd.cut(
        model["area_total_ha"],
        bins=[-float("inf"), 2, 5, float("inf")],
        labels=["pequeno_<2ha", "mediano_2_5ha", "grande_>5ha"],
    )

    model.to_parquet(MODEL_OUTPUT, index=False)
    model.to_csv(MODEL_CSV, index=False)

    audit_rows = []
    audit_rows.append(
        {
            "variable": "labor_total",
            "components": ",".join(labor_cols),
            **component_missingness(model, labor_cols),
        }
    )
    input_cols = ["gasto_abono", "gasto_fertilizantes", "gasto_plaguicidas"]
    audit_rows.append(
        {
            "variable": "input_costs",
            "components": ",".join(input_cols),
            **component_missingness(model, input_cols),
        }
    )
    audit_rows.append(
        {
            "variable": "practice_any",
            "components": ",".join(PRACTICE_ANY_VARS),
            **practice_missingness,
        }
    )
    audit_rows.append(
        {
            "variable": "num_practices",
            "components": ",".join(PRACTICE_ANY_VARS),
            **practice_missingness,
        }
    )
    audit = pd.DataFrame(audit_rows)
    audit.to_csv(OUTPUT_TABLES / "19_missingness_audit.csv", index=False)

    print("Wrote model_data_ena2024.parquet, model_data_ena2024.csv, and missingness audit")

model.head()

# %% [markdown]
# ### Quick model checks

# %%
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

missing = {var: float(model[var].isna().mean()) for var in key_vars if var in model.columns}
missing

# %%
plt.figure(figsize=(6, 4))
sns.scatterplot(
    data=model.sample(min(5000, len(model)), random_state=42),
    x="labor_total",
    y="input_costs",
    hue="size_cat",
    alpha=0.5,
)
plt.title("Labor vs input costs (sample)")
plt.tight_layout()
if SAVE_PLOTS:
    plt.savefig(OUTPUT_TABLES / "labor_vs_inputs.png", dpi=200)
plt.show()

# %% [markdown]
# ## 7. Build ENA controls (irrigation, machinery, seed, credit, education)
#
# We reproduce the control-feature logic from `src/features/ena_controls.py` but
# inline it for transparency.

# %%
ID_COLS = ["anio", "ccdd", "ccpp", "ccdi", "psu", "id_prod", "ua"]


def yes_no_dummy(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    out = pd.Series(pd.NA, index=series.index, dtype="Int64")
    out.loc[numeric == 1] = 1
    out.loc[numeric.isin([0, 2])] = 0
    return out


def add_missing_indicator(df: pd.DataFrame, col: str) -> None:
    df[f"{col}_missing"] = df[col].isna().astype(int)


def fill_zero_if_no(df: pd.DataFrame, indicator_col: str, value_cols: list[str]) -> None:
    if indicator_col not in df.columns:
        return
    mask_no = df[indicator_col].fillna(-1).eq(0)
    for col in value_cols:
        if col in df.columns:
            df.loc[mask_no, col] = df.loc[mask_no, col].fillna(0)


def load_variable_map() -> dict[str, str]:
    with (INTERMEDIATE_DIR / "variable_map.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_module(path: Path, raw_cols: list[str], variable_map: dict[str, str]) -> pd.DataFrame:
    df = read_csv(path, usecols=raw_cols, low_memory=False)
    df = normalize_columns(df)
    rename_map = {raw: variable_map.get(raw, raw) for raw in raw_cols}
    df = df.rename(columns=rename_map)
    return coerce_keys(df, ID_COLS)


def irrigation_features(variable_map: dict[str, str]) -> pd.DataFrame:
    schema_cols = ID_COLS + ["water_source", "irrigation_system"]
    schema = pd.read_parquet(INTERMEDIATE_DIR / "ena2024_schema.parquet", columns=schema_cols)
    schema = coerce_keys(schema, ID_COLS)

    water_source = pd.to_numeric(schema["water_source"], errors="coerce")
    irrigation_system = pd.to_numeric(schema["irrigation_system"], errors="coerce")

    schema["riego_crop"] = pd.Series(pd.NA, index=schema.index, dtype="Int64")
    schema.loc[water_source.notna(), "riego_crop"] = (water_source[water_source.notna()] != 1).astype(int)
    schema["riego_tecnificado_crop"] = pd.Series(pd.NA, index=schema.index, dtype="Int64")
    schema.loc[irrigation_system.notna(), "riego_tecnificado_crop"] = irrigation_system[
        irrigation_system.notna()
    ].isin([1, 2, 3, 4, 5, 6]).astype(int)

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
    add_missing_indicator(cap800, "usuario_agua")
    cap800 = cap800[ID_COLS + ["usuario_agua"]].drop_duplicates(subset=ID_COLS)

    cap1000_path = RAW_DIR / "973-Modulo1910" / "18_CAP1000.csv"
    cap1000_cols = ["ANIO", "CCDD", "CCPP", "CCDI", "NSEGM", "ID_PROD", "UA", "P1001A_3"]
    cap1000 = load_module(cap1000_path, cap1000_cols, variable_map)
    cap1000["gasto_agua_riego"] = pd.to_numeric(cap1000["gasto_agua_riego"], errors="coerce")
    cap1000 = cap1000[ID_COLS + ["gasto_agua_riego"]].drop_duplicates(subset=ID_COLS)

    merged = crop_agg.merge(cap800, on=ID_COLS, how="left").merge(cap1000, on=ID_COLS, how="left")
    fill_zero_if_no(merged, "usuario_agua", ["gasto_agua_riego"])
    add_missing_indicator(merged, "riego_any")
    add_missing_indicator(merged, "riego_tecnificado_any")
    add_missing_indicator(merged, "usuario_agua")

    return merged


def machinery_capital_features(variable_map: dict[str, str]) -> pd.DataFrame:
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
    add_missing_indicator(cap1000, "uso_maquinaria")
    for col in ["gasto_compra_equipos", "gasto_compra_maquinaria", "gasto_alquiler_mant_equipos"]:
        cap1000[col] = pd.to_numeric(cap1000[col], errors="coerce")
    fill_zero_if_no(
        cap1000,
        "uso_maquinaria",
        ["gasto_compra_equipos", "gasto_compra_maquinaria", "gasto_alquiler_mant_equipos"],
    )
    cap1000 = cap1000[
        ID_COLS
        + ["uso_maquinaria", "gasto_compra_equipos", "gasto_compra_maquinaria", "gasto_alquiler_mant_equipos"]
    ]

    cap1200_path = RAW_DIR / "973-Modulo1913" / "21_CAP1200B_ME.csv"
    cap1200_cols = ["ANIO", "CCDD", "CCPP", "CCDI", "NSEGM", "ID_PROD", "UA", "P1207_N"]
    cap1200 = load_module(cap1200_path, cap1200_cols, variable_map)
    cap1200["num_maquinaria_equipo"] = pd.to_numeric(cap1200["num_maquinaria_equipo"], errors="coerce")
    cap1200_agg = (
        cap1200.groupby(ID_COLS, dropna=False)["num_maquinaria_equipo"].sum(min_count=1).reset_index()
    )

    merged = cap1000.merge(cap1200_agg, on=ID_COLS, how="left")
    add_missing_indicator(merged, "uso_maquinaria")

    return merged


def fertilizer_seed_features(variable_map: dict[str, str]) -> pd.DataFrame:
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
    cap200e["gasto_semilla"] = pd.to_numeric(cap200e["gasto_semilla"], errors="coerce")
    cap200e["semilla_semillero"] = yes_no_dummy(cap200e["semilla_semillero"])
    cap200e["semilla_comercial"] = yes_no_dummy(cap200e["semilla_comercial"])
    cap200e["usa_abono"] = yes_no_dummy(cap200e["usa_abono"])
    cap200e["usa_fertilizantes"] = yes_no_dummy(cap200e["usa_fertilizantes"])

    cap200e_agg = (
        cap200e.groupby(ID_COLS, dropna=False)
        .agg(
            gasto_semilla=("gasto_semilla", lambda x: x.sum(min_count=1)),
            usa_abono=("usa_abono", "max"),
            usa_fertilizantes=("usa_fertilizantes", "max"),
            semilla_semillero_any=("semilla_semillero", "max"),
            semilla_comercial_any=("semilla_comercial", "max"),
        )
        .reset_index()
    )

    schema_cols = ID_COLS + ["seed_certified"]
    schema = pd.read_parquet(INTERMEDIATE_DIR / "ena2024_schema.parquet", columns=schema_cols)
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

    merged = cap200e_agg.merge(seed_agg, on=ID_COLS, how="left")
    for col in [
        "usa_abono",
        "usa_fertilizantes",
        "semilla_semillero_any",
        "semilla_comercial_any",
        "semilla_certificada_any",
    ]:
        add_missing_indicator(merged, col)

    return merged


def extension_credit_education_features(variable_map: dict[str, str]) -> pd.DataFrame:
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
    cap800["asociacion_num"] = pd.to_numeric(cap800["asociacion_num"], errors="coerce")
    fill_zero_if_no(cap800, "asociacion_miembro", ["asociacion_num"])
    cap800 = cap800[ID_COLS + ["asociacion_miembro", "asociacion_num"]].drop_duplicates(subset=ID_COLS)

    merged = cap700.merge(cap900, on=ID_COLS, how="left")
    merged = merged.merge(cap1100, on=ID_COLS, how="left")
    merged = merged.merge(cap800, on=ID_COLS, how="left")

    for col in ["capacitacion_recibida", "asistencia_tecnica_recibida", "credito_obtenido", "asociacion_miembro"]:
        add_missing_indicator(merged, col)
    add_missing_indicator(merged, "asociacion_num")

    return merged


PLUS_CONTROLS_OUTPUT = PROCESSED_DIR / "model_data_ena2024_plus_controls.parquet"
PLUS_CONTROLS_CSV = PROCESSED_DIR / "model_data_ena2024_plus_controls.csv"

if maybe_use_cache([PLUS_CONTROLS_OUTPUT, PLUS_CONTROLS_CSV]):
    model_plus = pd.read_parquet(PLUS_CONTROLS_OUTPUT)
    print("[cache] plus controls: using existing outputs")
else:
    ensure_dir(PROCESSED_DIR)
    ensure_dir(OUTPUT_TABLES)

    variable_map = load_variable_map()

    controls_frames = [
        irrigation_features(variable_map),
        machinery_capital_features(variable_map),
        fertilizer_seed_features(variable_map),
        extension_credit_education_features(variable_map),
    ]

    model_plus = model.copy()
    for controls in controls_frames:
        for col in ID_COLS:
            if col in controls.columns:
                controls[col] = controls[col].astype("string").str.replace(r"\.0$", "", regex=True)
        model_plus = model_plus.merge(controls, on=ID_COLS, how="left")

    model_plus.to_parquet(PLUS_CONTROLS_OUTPUT, index=False)
    model_plus.to_csv(PLUS_CONTROLS_CSV, index=False)

    control_cols = [
        "riego_any",
        "riego_share",
        "riego_tecnificado_any",
        "riego_tecnificado_share",
        "usuario_agua",
        "gasto_agua_riego",
        "uso_maquinaria",
        "num_maquinaria_equipo",
        "gasto_compra_equipos",
        "gasto_compra_maquinaria",
        "gasto_alquiler_mant_equipos",
        "gasto_semilla",
        "usa_abono",
        "usa_fertilizantes",
        "semilla_semillero_any",
        "semilla_comercial_any",
        "semilla_certificada_any",
        "semilla_certificada_share",
        "capacitacion_recibida",
        "asistencia_tecnica_recibida",
        "credito_obtenido",
        "nivel_educacion",
        "asociacion_miembro",
        "asociacion_num",
    ]

    def summarize_controls(df: pd.DataFrame, variables: list[str]) -> pd.DataFrame:
        summary_rows = []
        group_specs = [("overall", None), ("region", "region_natural"), ("size", "size_cat")]

        for group_type, group_col in group_specs:
            if group_col is None:
                groups = [("overall", df)]
            else:
                grouped = df.copy()
                grouped["_group"] = grouped[group_col].astype(object)
                grouped["_group"] = grouped["_group"].where(grouped["_group"].notna(), "missing")
                groups = list(grouped.groupby("_group", dropna=False))
            for group, gdf in groups:
                for var in variables:
                    series = pd.to_numeric(gdf[var], errors="coerce")
                    summary_rows.append(
                        {
                            "group_type": group_type,
                            "group": group,
                            "variable": var,
                            "missing_pct": float(series.isna().mean()),
                            "mean": float(series.mean()) if series.notna().any() else float("nan"),
                            "p50": float(series.quantile(0.5)) if series.notna().any() else float("nan"),
                            "p90": float(series.quantile(0.9)) if series.notna().any() else float("nan"),
                        }
                    )

        return pd.DataFrame(summary_rows)

    coverage = summarize_controls(model_plus, control_cols)
    coverage.to_csv(OUTPUT_TABLES / "11_controls_ena_coverage.csv", index=False)
    (OUTPUT_TABLES / "11_controls_ena_coverage.md").write_text(to_markdown(coverage), encoding="utf-8")

    print("Wrote model_data_ena2024_plus_controls.parquet and controls coverage tables")

model_plus.head()

# %% [markdown]
# ### Controls snapshot plot

# %%
plt.figure(figsize=(6, 4))
sns.histplot(model_plus["riego_share"].dropna(), bins=30)
plt.title("Irrigation share distribution")
plt.tight_layout()
if SAVE_PLOTS:
    plt.savefig(OUTPUT_TABLES / "irrigation_share_hist.png", dpi=200)
plt.show()

# %% [markdown]
# ## 8. Merge external geo + climate features (optional)
#
# If external processed files are available, we merge them to build
# `plus_geo`, `plus_controls_temp`, and `plus_geo2` datasets.

# %%

def build_ubigeo6(df: pd.DataFrame) -> pd.Series:
    ccdd = pd.to_numeric(df["ccdd"], errors="coerce").round().astype("Int64").astype("string").str.zfill(2)
    ccpp = pd.to_numeric(df["ccpp"], errors="coerce").round().astype("Int64").astype("string").str.zfill(2)
    ccdi = pd.to_numeric(df["ccdi"], errors="coerce").round().astype("Int64").astype("string").str.zfill(2)
    ubigeo6 = (ccdd + ccpp + ccdi).where(~(df["ccdd"].isna() | df["ccpp"].isna() | df["ccdi"].isna()))
    return ubigeo6


# -- plus_geo: base model + ubigeo + CHIRPS
ubigeo_path = EXTERNAL_DIR / "ubigeo_district_capitals.parquet"
chirps_path = EXTERNAL_DIR / "chirps_district_features_2024.parquet"

if ubigeo_path.exists() and chirps_path.exists() and MODEL_OUTPUT.exists():
    model_geo = model.copy()
    model_geo["ubigeo6"] = build_ubigeo6(model_geo)

    ubigeo = pd.read_parquet(ubigeo_path)
    chirps = pd.read_parquet(chirps_path)

    merged_geo = model_geo.merge(ubigeo, on="ubigeo6", how="left", suffixes=("", "_ubigeo"))
    merged_geo = merged_geo.merge(chirps, on="ubigeo6", how="left")

    for base in ["ccdd", "ccpp", "ccdi", "departamento", "provincia", "distrito"]:
        ubigeo_col = f"{base}_ubigeo"
        if ubigeo_col in merged_geo.columns and base in merged_geo.columns:
            merged_geo = merged_geo.drop(columns=[ubigeo_col])

    merged_geo.to_parquet(PROCESSED_DIR / "model_data_ena2024_plus_geo.parquet", index=False)
    merged_geo.to_csv(PROCESSED_DIR / "model_data_ena2024_plus_geo.csv", index=False)

    summary_frames = []
    summary_frames.append(merged_geo.assign(group_type="overall", group="overall"))
    summary_frames.append(merged_geo.assign(group_type="region", group=merged_geo["region_natural"].astype("string")))

    coverage_geo = (
        pd.concat(summary_frames, ignore_index=True)
        .groupby(["group_type", "group"], dropna=False)
        .agg(
            n=("id_prod", "count"),
            share_geo_match=("capital_lat", lambda x: x.notna().mean()),
            share_chirps_match=("prcp_2024_total", lambda x: x.notna().mean()),
            mean_prcp_total_z=("prcp_total_z", "mean"),
            sd_prcp_total_z=("prcp_total_z", "std"),
        )
        .reset_index()
    )

    coverage_geo.to_csv(OUTPUT_TABLES / "06_geo_feature_coverage.csv", index=False)
    (OUTPUT_TABLES / "06_geo_feature_coverage.md").write_text(to_markdown(coverage_geo), encoding="utf-8")

    print("Wrote model_data_ena2024_plus_geo.parquet and coverage table")
else:
    print("External geo data not found; skipping plus_geo build")


# -- plus_controls_temp: add temperature features

TEMP_PATH = EXTERNAL_DIR / "temperature_district_features_2023_2024.parquet"

if TEMP_PATH.exists() and PLUS_CONTROLS_OUTPUT.exists():
    temp_model = model_plus.copy()
    temp_model["ubigeo6"] = build_ubigeo6(temp_model)
    temp = pd.read_parquet(TEMP_PATH)

    merged_temp = temp_model.merge(temp, on="ubigeo6", how="left")
    merged_temp.to_parquet(PROCESSED_DIR / "model_data_ena2024_plus_controls_temp.parquet", index=False)
    merged_temp.to_csv(PROCESSED_DIR / "model_data_ena2024_plus_controls_temp.csv", index=False)

    summary_frames = []
    summary_frames.append(merged_temp.assign(group_type="overall", group="overall"))
    summary_frames.append(merged_temp.assign(group_type="region", group=merged_temp["region_natural"].astype("string")))

    coverage_temp = (
        pd.concat(summary_frames, ignore_index=True)
        .groupby(["group_type", "group"], dropna=False)
        .agg(
            n=("id_prod", "count"),
            share_temp_match=("tmean_2024", lambda x: x.notna().mean()),
            mean_tmean_2024=("tmean_2024", "mean"),
            mean_tmean_2023=("tmean_2023", "mean"),
            mean_delta_tmean=("delta_tmean_24_23", "mean"),
        )
        .reset_index()
    )

    coverage_temp.to_csv(OUTPUT_TABLES / "12_temp_topo_coverage.csv", index=False)
    (OUTPUT_TABLES / "12_temp_topo_coverage.md").write_text(to_markdown(coverage_temp), encoding="utf-8")

    print("Wrote model_data_ena2024_plus_controls_temp.parquet and temp coverage table")
else:
    print("Temperature features not found; skipping plus_controls_temp build")


# -- plus_geo2: add ubigeo + CHIRPS + topography

TOPO_PATH = EXTERNAL_DIR / "topography_district_features.parquet"

if TOPO_PATH.exists() and (PROCESSED_DIR / "model_data_ena2024_plus_controls_temp.parquet").exists():
    geo2_base = pd.read_parquet(PROCESSED_DIR / "model_data_ena2024_plus_controls_temp.parquet")
    geo2_base["ubigeo6"] = build_ubigeo6(geo2_base)

    ubigeo = pd.read_parquet(ubigeo_path) if ubigeo_path.exists() else None
    chirps = pd.read_parquet(chirps_path) if chirps_path.exists() else None
    topo = pd.read_parquet(TOPO_PATH)

    merged_geo2 = geo2_base
    if ubigeo is not None:
        merged_geo2 = merged_geo2.merge(ubigeo, on="ubigeo6", how="left", suffixes=("", "_ubigeo"))
    if chirps is not None:
        merged_geo2 = merged_geo2.merge(chirps, on="ubigeo6", how="left")
    merged_geo2 = merged_geo2.merge(topo, on="ubigeo6", how="left")

    for base in ["ccdd", "ccpp", "ccdi", "departamento", "provincia", "distrito"]:
        ubigeo_col = f"{base}_ubigeo"
        if ubigeo_col in merged_geo2.columns and base in merged_geo2.columns:
            merged_geo2 = merged_geo2.drop(columns=[ubigeo_col])

    merged_geo2.to_parquet(PROCESSED_DIR / "model_data_ena2024_plus_geo2.parquet", index=False)
    merged_geo2.to_csv(PROCESSED_DIR / "model_data_ena2024_plus_geo2.csv", index=False)

    summary_frames = []
    summary_frames.append(merged_geo2.assign(group_type="overall", group="overall"))
    summary_frames.append(merged_geo2.assign(group_type="region", group=merged_geo2["region_natural"].astype("string")))

    coverage_geo2 = (
        pd.concat(summary_frames, ignore_index=True)
        .groupby(["group_type", "group"], dropna=False)
        .agg(
            n=("id_prod", "count"),
            share_temp_match=("tmean_2024", lambda x: x.notna().mean()),
            mean_tmean_2024=("tmean_2024", "mean"),
            mean_tmean_2023=("tmean_2023", "mean"),
            mean_delta_tmean=("delta_tmean_24_23", "mean"),
            share_topo_match=("elev_m", lambda x: x.notna().mean()),
            mean_elev_m=("elev_m", "mean"),
            mean_slope_deg=("slope_deg", "mean"),
            mean_ruggedness=("ruggedness", "mean"),
        )
        .reset_index()
    )

    coverage_geo2.to_csv(OUTPUT_TABLES / "12_temp_topo_coverage.csv", index=False)
    (OUTPUT_TABLES / "12_temp_topo_coverage.md").write_text(to_markdown(coverage_geo2), encoding="utf-8")

    print("Wrote model_data_ena2024_plus_geo2.parquet and geo2 coverage table")
else:
    print("Topography or temp data not found; skipping plus_geo2 build")

# %% [markdown]
# ### Climate scatter (if available)

# %%
if "merged_temp" in globals():
    plot_df = merged_temp.sample(min(5000, len(merged_temp)), random_state=42)
    if {"tmean_2024", "delta_tmean_24_23"}.issubset(plot_df.columns):
        x_col = "tmean_2024"
        y_col = "delta_tmean_24_23"
        title = "Temperature level vs change (sample)"
    elif {"tmean_2024", "tmean_2023"}.issubset(plot_df.columns):
        x_col = "tmean_2024"
        y_col = "tmean_2023"
        title = "Temperature 2024 vs 2023 (sample)"
    elif {"tmean_2024", "prcp_2024_total"}.issubset(plot_df.columns):
        x_col = "tmean_2024"
        y_col = "prcp_2024_total"
        title = "Temperature vs precipitation (sample)"
    else:
        x_col = None
        y_col = None
        title = None

    if x_col and y_col:
        plt.figure(figsize=(6, 4))
        sns.scatterplot(data=plot_df, x=x_col, y=y_col, alpha=0.5)
        plt.title(title)
        plt.tight_layout()
        if SAVE_PLOTS:
            plt.savefig(OUTPUT_TABLES / "temp_scatter.png", dpi=200)
        plt.show()

# %% [markdown]
# ## 9. Final outputs summary
#
# We list the primary outputs written by this notebook.

# %%
outputs = [
    INTERMEDIATE_DIR / "module_profile.csv",
    INTERMEDIATE_DIR / "ena2024_raw.parquet",
    INTERMEDIATE_DIR / "ena2024_dictionary.csv",
    INTERMEDIATE_DIR / "variable_map.json",
    INTERMEDIATE_DIR / "ena2024_schema.parquet",
    PROCESSED_DIR / "ena2024_features.parquet",
    PROCESSED_DIR / "model_data_ena2024.parquet",
    PROCESSED_DIR / "model_data_ena2024_plus_controls.parquet",
    PROCESSED_DIR / "model_data_ena2024_plus_geo.parquet",
    PROCESSED_DIR / "model_data_ena2024_plus_controls_temp.parquet",
    PROCESSED_DIR / "model_data_ena2024_plus_geo2.parquet",
]

for path in outputs:
    status = "OK" if path.exists() else "missing"
    print(f"{status:>7}  {path.relative_to(REPO_ROOT)}")

# %% [markdown]
# ## Notes and next steps
#
# - The outputs mirror the Python pipeline scripts, but are generated directly
#   inside this notebook for clarity.
# - If you want to force a rebuild, set `FORCE_REBUILD = True` at the top.
# - The resulting datasets are ready for EDA, modeling, and report generation.
