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
# # 01 - Data ingestion and cleaning
#
# This notebook documents how raw ENA 2024 files are profiled, standardized,
# and transformed into the core modeling dataset. It mirrors the pipeline
# scripts in `src/ena/` while adding narrative context for researchers.
#
# **Design choice:** expensive steps are guarded by cache checks so the notebook
# can reuse existing outputs and avoid long downloads or recomputation.

# %%
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys

import numpy as np
import pandas as pd

# %% [markdown]
# ## Setup and configuration
#
# Toggle flags below depending on whether you want to rebuild artifacts or
# reuse cached outputs.

# %%
USE_CACHED = True
FORCE_REBUILD = False


def find_repo_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    for parent in [start] + list(start.parents):
        if (parent / "src").exists() and (parent / "data").exists():
            return parent
    raise RuntimeError("Could not locate repo root. Run from within the repo.")


REPO_ROOT = find_repo_root()
PYTHON = sys.executable

RAW_DIR = REPO_ROOT / "data" / "raw" / "ENA_2024"
INTERMEDIATE_DIR = REPO_ROOT / "data" / "intermediate"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
OUTPUT_TABLES = REPO_ROOT / "outputs" / "tables"


def run_cmd(cmd: list[str]) -> None:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def ensure_outputs(outputs: list[Path], cmd: list[str], label: str) -> None:
    outputs = [Path(p) for p in outputs]
    if USE_CACHED and not FORCE_REBUILD and all(p.exists() for p in outputs):
        print(f"[cache] {label}: using existing outputs")
        return
    run_cmd(cmd)


# %% [markdown]
# ## Raw data availability
#
# The ENA files are expected under `data/raw/ENA_2024`. We check that the
# directory exists and report how many CSVs are available.

# %%
if not RAW_DIR.exists():
    raise FileNotFoundError(f"Missing raw data folder: {RAW_DIR}")

csv_count = len(list(RAW_DIR.rglob("*.csv")))
print(f"Raw ENA CSV files found: {csv_count}")

# %% [markdown]
# ## Step 1: repo inventory and module profiling
#
# These scripts scan raw data and write summaries to `docs/` and
# `data/intermediate/`.

# %%
ensure_outputs(
    outputs=[REPO_ROOT / "docs" / "REPO_INVENTORY.md", INTERMEDIATE_DIR / "raw_manifest.csv"],
    cmd=[PYTHON, "src/ena/scan_repo.py"],
    label="scan_repo",
)

ensure_outputs(
    outputs=[INTERMEDIATE_DIR / "module_profile.csv", INTERMEDIATE_DIR / "ena2024_raw.parquet"],
    cmd=[PYTHON, "src/ena/01_load_and_profile.py"],
    label="load_and_profile",
)

# %% [markdown]
# ## Step 2: build a standardized schema from the PDF dictionary
#
# This step parses the official PDF dictionary and writes:
# - `data/intermediate/ena2024_dictionary.csv`
# - `data/intermediate/variable_map.json`
# - `docs/ENA2024_VARIABLE_DICTIONARY.md`

# %%
ensure_outputs(
    outputs=[
        INTERMEDIATE_DIR / "ena2024_dictionary.csv",
        INTERMEDIATE_DIR / "variable_map.json",
        REPO_ROOT / "docs" / "ENA2024_VARIABLE_DICTIONARY.md",
    ],
    cmd=[PYTHON, "src/ena/02_build_schema_from_dictionary.py"],
    label="build_schema_from_dictionary",
)

# %% [markdown]
# ## Step 3: apply schema to crop and cover modules
#
# The merged long dataset (`ena2024_schema.parquet`) combines crop records with
# household metadata and standard variable names.

# %%
ensure_outputs(
    outputs=[INTERMEDIATE_DIR / "ena2024_schema.parquet"],
    cmd=[PYTHON, "src/ena/03_apply_schema.py"],
    label="apply_schema",
)

# %% [markdown]
# ## Step 4: compute diversification indices
#
# This produces producer-level diversification measures (HHI, Shannon, etc.)
# and writes the base feature table.

# %%
ensure_outputs(
    outputs=[PROCESSED_DIR / "ena2024_features.parquet", OUTPUT_TABLES / "01_diversification_descriptives.csv"],
    cmd=[PYTHON, "src/ena/04_compute_diversification.py"],
    label="compute_diversification",
)

# %% [markdown]
# ## Step 5: build model dataset with practices
#
# The practice outcome uses the subset:
# P301A_1--4C, P301A_11, P301A_16, P301A_17
#
# This step writes `model_data_ena2024.parquet` and `model_data_ena2024.csv`.

# %%
ensure_outputs(
    outputs=[PROCESSED_DIR / "model_data_ena2024.parquet", PROCESSED_DIR / "model_data_ena2024.csv"],
    cmd=[PYTHON, "src/ena/05_build_model_data.py"],
    label="build_model_data",
)

# %% [markdown]
# ## Step 6: add ENA controls
#
# This joins irrigation, machinery, seed, extension, and credit controls. The
# resulting dataset is used in extended specifications.

# %%
ensure_outputs(
    outputs=[
        PROCESSED_DIR / "model_data_ena2024_plus_controls.parquet",
        PROCESSED_DIR / "model_data_ena2024_plus_controls.csv",
        OUTPUT_TABLES / "11_controls_ena_coverage.csv",
    ],
    cmd=[PYTHON, "src/ena/06_build_model_data_plus_controls.py"],
    label="build_model_data_plus_controls",
)

# %% [markdown]
# ## Quick validation checks
#
# We inspect the core dataset, summarize missingness, and confirm the new
# practice definition produces expected prevalence.

# %%
model = pd.read_parquet(PROCESSED_DIR / "model_data_ena2024.parquet")

key_vars = [
    "valor_total",
    "area_total_ha",
    "diversificacion_area",
    "practice_any",
    "num_practices",
    "weight",
]

missing = {col: float(model[col].isna().mean()) for col in key_vars if col in model.columns}
print("Missing share:", missing)

practice_mean = float(model["practice_any"].mean())
print(f"practice_any mean: {practice_mean:.4f}")

model[key_vars].describe(include="all")

# %% [markdown]
# ## Interpretation
#
# - The base dataset is ready for EDA and modeling.
# - Practice prevalence is lower than the original all-P301A definition,
#   reducing saturation and improving interpretability.
# - If any required output is missing, set `FORCE_REBUILD = True` to rebuild.
