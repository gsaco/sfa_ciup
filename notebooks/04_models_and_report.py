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
# # 04 - Modeling (SFA + logit) and reporting
#
# This notebook runs the econometric models and summarizes key outputs.
# It relies on cached outputs when available to avoid long runtimes.

# %%
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys

import pandas as pd

# %% [markdown]
# ## Setup

# %%
USE_CACHED = True
RUN_MODELS = False
RUN_REPORT = False


def find_repo_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    for parent in [start] + list(start.parents):
        if (parent / "src").exists() and (parent / "data").exists():
            return parent
    raise RuntimeError("Could not locate repo root. Run from within the repo.")


REPO_ROOT = find_repo_root()
PYTHON = sys.executable

OUTPUT_TABLES = REPO_ROOT / "outputs" / "tables"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"


def run_cmd(cmd: list[str]) -> None:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def ensure_or_skip(outputs: list[Path], cmd: list[str], label: str) -> None:
    outputs = [Path(p) for p in outputs]
    if USE_CACHED and all(p.exists() for p in outputs):
        print(f"[cache] {label}: using existing outputs")
        return
    if not RUN_MODELS:
        print(f"[skip] {label}: outputs missing, set RUN_MODELS=True to run")
        return
    run_cmd(cmd)


# %% [markdown]
# ## Run SFA and logit models (optional)
#
# These steps call the R scripts directly. Set `RUN_MODELS = True` to re-run.

# %%
rscript = shutil.which("Rscript")
if rscript is None:
    print("Rscript not found. Model estimation will be skipped.")
else:
    ensure_or_skip(
        outputs=[OUTPUT_TABLES / "02_sfa_main.csv", OUTPUT_TABLES / "03_sfa_robustness.csv"],
        cmd=["Rscript", "R/01_sfa_main.R"],
        label="SFA",
    )
    ensure_or_skip(
        outputs=[OUTPUT_TABLES / "04_logit_main.csv", OUTPUT_TABLES / "05_logit_robustness.csv"],
        cmd=["Rscript", "R/02_logit_practices.R"],
        label="Logit",
    )

# %% [markdown]
# ## Sample loss analysis
#
# This step recomputes sample retention when adding geo/climate variables.

# %%
ensure_or_skip(
    outputs=[OUTPUT_TABLES / "sample_loss_analysis.csv"],
    cmd=[PYTHON, "src/qa/sample_loss_analysis.py"],
    label="sample_loss_analysis",
)

# %% [markdown]
# ## Load model outputs

# %%
logit_main_path = OUTPUT_TABLES / "04_logit_main.csv"
logit_controls_path = OUTPUT_TABLES / "16_logit_with_controls_ena.csv"
logit_compare_path = OUTPUT_TABLES / "18_logit_compare_effects_all.csv"

sfa_main_path = OUTPUT_TABLES / "02_sfa_main.csv"

if logit_main_path.exists():
    logit_main = pd.read_csv(logit_main_path)
    logit_main.head()
else:
    logit_main = None

# %% [markdown]
# ## Logit summary (practice_any)
#
# The outcome uses P301A_1--4C, P301A_11, P301A_16, P301A_17.

# %%
if logit_main is not None:
    key_terms = [
        "diversificacion_area",
        "region_natural2",
        "region_natural3",
        "diversificacion_area:size_catmediano_2_5ha",
        "diversificacion_area:size_catpequeno_<2ha",
    ]
    logit_main[logit_main["term"].isin(key_terms)]

# %% [markdown]
# ## SFA summary
#
# The SFA is unweighted (package limitation). We highlight main coefficients
# from the inefficiency equation when available.

# %%
if sfa_main_path.exists():
    sfa_main = pd.read_csv(sfa_main_path)
    sfa_main.head()

# %% [markdown]
# ## Optional: regenerate the report
#
# This uses `src/report/build_report.py` and (optionally) compiles the LaTeX
# report. Set `RUN_REPORT = True` if you want to update `reports/informe.tex`.

# %%
if RUN_REPORT:
    run_cmd([PYTHON, "src/report/build_report.py"])
    pdflatex = shutil.which("pdflatex")
    if pdflatex is not None:
        run_cmd([
            "pdflatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-output-directory",
            "reports",
            "reports/informe.tex",
        ])
    else:
        print("pdflatex not found; skipping PDF compile")

# %% [markdown]
# ## Interpretation
#
# - Diversification remains positively associated with practice adoption under
#   the updated outcome definition.
# - The SFA results should be interpreted cautiously due to known convergence
#   warnings and the lack of survey weights.
# - Use the compare tables in `outputs/tables/` to examine sensitivity across
#   specifications.
