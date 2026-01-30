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
# # 02 - Exploratory data analysis (extended)
#
# This notebook expands the exploratory analysis to cover a broader set of
# variables, including the controls module (irrigation, machinery, seed use,
# training/credit/education). It focuses on distributional patterns, missingness,
# group differences, and simple bivariate relationships that motivate modeling
# choices.

# %%
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# %% [markdown]
# ## Setup

# %%
SAVE_PLOTS = False
RANDOM_SEED = 42


def find_repo_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    for parent in [start] + list(start.parents):
        if (parent / "src").exists() and (parent / "data").exists():
            return parent
    raise RuntimeError("Could not locate repo root. Run from within the repo.")


REPO_ROOT = find_repo_root()
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
PLOT_DIR = REPO_ROOT / "outputs" / "plots" / "notebooks"
PLOT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 110


ID_COLS = ["anio", "ccdd", "ccpp", "ccdi", "psu", "id_prod", "ua"]


def weighted_mean(series: pd.Series, weights: pd.Series) -> float:
    mask = series.notna() & weights.notna()
    if not mask.any():
        return float("nan")
    return float((series[mask] * weights[mask]).sum() / weights[mask].sum())


def safe_ratio(numer: pd.Series, denom: pd.Series) -> pd.Series:
    out = numer / denom
    out = out.where((denom > 0) & denom.notna())
    return out


def share_zero(series: pd.Series) -> float:
    return float(series.eq(0).mean())


# %% [markdown]
# ## Load the modeling datasets
#
# We load the base model dataset and (if available) the plus-controls dataset
# to extend the analysis to irrigation, machinery, seed, and extension variables.

# %%
model_path = PROCESSED_DIR / "model_data_ena2024.parquet"
if not model_path.exists():
    raise FileNotFoundError(f"Missing model dataset: {model_path}")

model = pd.read_parquet(model_path)

controls_path = PROCESSED_DIR / "model_data_ena2024_plus_controls.parquet"
if controls_path.exists():
    model_ctrl = pd.read_parquet(controls_path)
    controls_loaded = True
else:
    model_ctrl = model.copy()
    controls_loaded = False

print("Base shape:", model.shape)
print("Controls shape:", model_ctrl.shape)
print("Controls loaded:", controls_loaded)

# %% [markdown]
# ## Data overview
#
# Quick structural checks for duplicates, key completeness, and sample sizes.

# %%
print("Duplicate key rows (base):", int(model.duplicated(subset=ID_COLS).sum()))
missing_keys = model[ID_COLS].isna().mean().sort_values(ascending=False)
print("Missingness in ID cols:\n", missing_keys)

region_counts = model["region_natural"].value_counts(dropna=False)
size_counts = model["size_cat"].value_counts(dropna=False)
print("\nRegion counts:\n", region_counts)
print("\nSize counts:\n", size_counts)

# %% [markdown]
# ## Core summary statistics
#
# Summary metrics for economic scale, diversification, and practice adoption.

# %%
summary_cols = [
    "valor_total",
    "area_total_ha",
    "labor_total",
    "input_costs",
    "diversificacion_area",
    "num_crops_area",
    "num_practices",
    "practice_any",
]

model[summary_cols].describe(percentiles=[0.05, 0.5, 0.95]).T

# %% [markdown]
# ## Missingness profile
#
# Missingness rates for key variables help contextualize later interpretations.

# %%
missing_targets = [
    "valor_total",
    "area_total_ha",
    "labor_total",
    "input_costs",
    "diversificacion_area",
    "num_crops_area",
    "practice_any",
]

missing_rates = model[missing_targets].isna().mean().sort_values(ascending=False)
missing_rates

# %%
fig, ax = plt.subplots(figsize=(6, 3))
missing_rates.plot(kind="bar", ax=ax, color="#4E79A7")
ax.set_title("Missing share (key variables)")
ax.set_ylabel("Share missing")
ax.set_ylim(0, max(0.02, missing_rates.max() * 1.2))
plt.tight_layout()
if SAVE_PLOTS:
    fig.savefig(PLOT_DIR / "eda_missingness_key_vars.png", dpi=150)

# %% [markdown]
# ## Derived intensity metrics
#
# We build per-hectare measures and log transforms for scale comparisons.

# %%
model = model.copy()

model["valor_por_ha"] = safe_ratio(model["valor_total"], model["area_total_ha"])
model["input_costs_por_ha"] = safe_ratio(model["input_costs"], model["area_total_ha"])
model["labor_por_ha"] = safe_ratio(model["labor_total"], model["area_total_ha"])

for col in ["valor_total", "area_total_ha", "input_costs", "labor_total"]:
    model[f"log1p_{col}"] = np.log1p(model[col].where(model[col] >= 0))

model[["valor_por_ha", "input_costs_por_ha", "labor_por_ha"]].describe(percentiles=[0.05, 0.5, 0.95]).T

# %% [markdown]
# ## Distribution of farm sizes and regions
#
# Understanding the sample composition helps interpret regional and scale effects.

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

sns.countplot(
    data=model,
    x="region_natural",
    order=region_counts.index,
    ax=axes[0],
    color="#59A14F",
)
axes[0].set_title("Observations by region")
axes[0].set_xlabel("region_natural")
axes[0].tick_params(axis="x", rotation=30)

sns.countplot(
    data=model,
    x="size_cat",
    order=size_counts.index,
    ax=axes[1],
    color="#F28E2B",
)
axes[1].set_title("Observations by size category")
axes[1].set_xlabel("size_cat")
axes[1].tick_params(axis="x", rotation=30)

plt.tight_layout()
if SAVE_PLOTS:
    fig.savefig(PLOT_DIR / "eda_counts_region_size.png", dpi=150)

# %% [markdown]
# ## Diversification metrics
#
# We summarize diversification through HHI-based measures and crop counts.

# %%
mono_share = float((model["num_crops_area"] == 1).mean())
zero_div_share = float((model["diversificacion_area"] == 0).mean())
print(f"Share monocrop (num_crops_area == 1): {mono_share:.3f}")
print(f"Share diversification == 0: {zero_div_share:.3f}")

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

sns.histplot(model["diversificacion_area"], bins=30, ax=axes[0], color="#4C78A8")
axes[0].set_title("Diversificacion (1 - HHI)")
axes[0].set_xlabel("diversificacion_area")

sns.histplot(model["num_crops_area"], bins=20, ax=axes[1], color="#72B7B2")
axes[1].set_title("Number of crops (area)")
axes[1].set_xlabel("num_crops_area")

plt.tight_layout()
if SAVE_PLOTS:
    fig.savefig(PLOT_DIR / "eda_diversification_distribution.png", dpi=150)

# %% [markdown]
# Diversification tends to show mass at zero when producers are specialized in
# a single crop, which is consistent with HHI = 1 for monocrop observations.

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

sns.boxplot(
    data=model,
    x="region_natural",
    y="diversificacion_area",
    ax=axes[0],
    color="#A0CBE8",
)
axes[0].set_title("Diversification by region")
axes[0].set_xlabel("region_natural")
axes[0].tick_params(axis="x", rotation=30)

sns.boxplot(
    data=model,
    x="size_cat",
    y="diversificacion_area",
    ax=axes[1],
    color="#FFBE7D",
)
axes[1].set_title("Diversification by size")
axes[1].set_xlabel("size_cat")
axes[1].tick_params(axis="x", rotation=30)

plt.tight_layout()
if SAVE_PLOTS:
    fig.savefig(PLOT_DIR / "eda_diversification_by_group.png", dpi=150)

# %% [markdown]
# ## Output distributions and intensity
#
# We examine the distribution of total value and value per hectare.

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

pos_val = model.loc[model["valor_total"] > 0, "valor_total"]
sns.histplot(np.log1p(pos_val), bins=30, ax=axes[0], color="#4E79A7")
axes[0].set_title("log1p(valor_total)")
axes[0].set_xlabel("log1p(valor_total)")

val_per_ha = model["valor_por_ha"].dropna()
sns.histplot(np.log1p(val_per_ha), bins=30, ax=axes[1], color="#59A14F")
axes[1].set_title("log1p(valor_por_ha)")
axes[1].set_xlabel("log1p(valor_por_ha)")

plt.tight_layout()
if SAVE_PLOTS:
    fig.savefig(PLOT_DIR / "eda_output_distribution.png", dpi=150)

# %% [markdown]
# Higher output levels are heavily right-skewed; log transforms are helpful for
# visualization and modeling.

# %%
sample_df = model[["diversificacion_area", "log1p_valor_total"]].dropna().sample(
    n=min(8000, len(model)), random_state=RANDOM_SEED
)

fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(sample_df["diversificacion_area"], sample_df["log1p_valor_total"], alpha=0.25, s=10)
ax.set_xlabel("diversificacion_area")
ax.set_ylabel("log1p(valor_total)")
ax.set_title("Diversification vs output (log)")

plt.tight_layout()
if SAVE_PLOTS:
    fig.savefig(PLOT_DIR / "eda_diversification_vs_output.png", dpi=150)

# %% [markdown]
# ## Labor and input costs
#
# We inspect labor and input expenditures, both in levels and per hectare.

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

sns.histplot(
    np.log1p(model["labor_total"].where(model["labor_total"] > 0)),
    bins=30,
    ax=axes[0],
    color="#EDC948",
)
axes[0].set_title("log1p(labor_total)")
axes[0].set_xlabel("log1p(labor_total)")

sns.histplot(
    np.log1p(model["input_costs"].where(model["input_costs"] > 0)),
    bins=30,
    ax=axes[1],
    color="#B07AA1",
)
axes[1].set_title("log1p(input_costs)")
axes[1].set_xlabel("log1p(input_costs)")

plt.tight_layout()
if SAVE_PLOTS:
    fig.savefig(PLOT_DIR / "eda_labor_inputs_distribution.png", dpi=150)

# %%
sample_df = model[["log1p_valor_total", "log1p_input_costs", "log1p_labor_total"]].dropna()
sample_df = sample_df.sample(n=min(8000, len(sample_df)), random_state=RANDOM_SEED)

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

axes[0].scatter(sample_df["log1p_input_costs"], sample_df["log1p_valor_total"], alpha=0.25, s=10)
axes[0].set_xlabel("log1p(input_costs)")
axes[0].set_ylabel("log1p(valor_total)")
axes[0].set_title("Inputs vs output")

axes[1].scatter(sample_df["log1p_labor_total"], sample_df["log1p_valor_total"], alpha=0.25, s=10)
axes[1].set_xlabel("log1p(labor_total)")
axes[1].set_ylabel("log1p(valor_total)")
axes[1].set_title("Labor vs output")

plt.tight_layout()
if SAVE_PLOTS:
    fig.savefig(PLOT_DIR / "eda_labor_inputs_vs_output.png", dpi=150)

# %% [markdown]
# ## Practice adoption
#
# The practices variable is based on a subset of practices captured in CAP300.
# We look at the distribution and group-level variation.

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

sns.histplot(model["num_practices"], bins=20, ax=axes[0], color="#59A14F")
axes[0].set_title("Number of practices (subset)")
axes[0].set_xlabel("num_practices")

practice_rates = model.groupby("region_natural", dropna=False)["practice_any"].mean().reset_index()
sns.barplot(data=practice_rates, x="region_natural", y="practice_any", ax=axes[1], color="#4E79A7")
axes[1].set_title("Practice adoption by region")
axes[1].set_xlabel("region_natural")
axes[1].set_ylabel("mean practice_any")
axes[1].tick_params(axis="x", rotation=30)

plt.tight_layout()
if SAVE_PLOTS:
    fig.savefig(PLOT_DIR / "eda_practices_distribution.png", dpi=150)

# %% [markdown]
# Practice adoption is heterogeneous across regions and size categories, which
# suggests value in interactions or stratified models.

# %%
size_practice = model.groupby("size_cat", dropna=False)["practice_any"].mean().reset_index()
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(data=size_practice, x="size_cat", y="practice_any", ax=ax, color="#F28E2B")
ax.set_title("Practice adoption by size")
ax.set_xlabel("size_cat")
ax.set_ylabel("mean practice_any")
ax.tick_params(axis="x", rotation=30)
plt.tight_layout()
if SAVE_PLOTS:
    fig.savefig(PLOT_DIR / "eda_practices_by_size.png", dpi=150)

# %% [markdown]
# ## Output by diversification bins
#
# Binning diversification helps identify non-linear patterns.

# %%
plot_df = model[["diversificacion_area", "log1p_valor_total"]].dropna()
plot_df = plot_df.loc[plot_df["diversificacion_area"].between(0, 1)]
plot_df = plot_df.assign(div_bin=pd.qcut(plot_df["diversificacion_area"], 5, duplicates="drop"))

bin_stats = plot_df.groupby("div_bin")["log1p_valor_total"].agg(["mean", "median", "count"]).reset_index()
bin_stats

# %%
fig, ax = plt.subplots(figsize=(6, 4))
sns.pointplot(data=bin_stats, x="div_bin", y="mean", ax=ax, color="#59A14F")
ax.set_title("Mean log1p(valor_total) by diversification quintile")
ax.set_xlabel("diversification bin")
ax.set_ylabel("mean log1p(valor_total)")
ax.tick_params(axis="x", rotation=30)
plt.tight_layout()
if SAVE_PLOTS:
    fig.savefig(PLOT_DIR / "eda_output_by_div_bins.png", dpi=150)

# %% [markdown]
# ## Weighted vs unweighted regional means
#
# ENA provides expansion weights. Comparing weighted and unweighted means can
# reveal how sampling affects aggregate estimates.

# %%
weighted_vars = ["valor_total", "diversificacion_area", "practice_any", "input_costs"]

weighted_rows = []
for region, gdf in model.groupby("region_natural", dropna=False):
    row = {"region_natural": region, "n": len(gdf)}
    for var in weighted_vars:
        row[f"mean_{var}"] = float(gdf[var].mean())
        row[f"wmean_{var}"] = weighted_mean(gdf[var], gdf["weight"])
    weighted_rows.append(row)

weighted_summary = pd.DataFrame(weighted_rows)
weighted_summary

# %% [markdown]
# ## Controls analysis (irrigation, machinery, seeds, services)
#
# When the plus-controls dataset is available, we summarize key controls and
# their prevalence. Missing indicators help identify reporting gaps.

# %%
if controls_loaded:
    ctrl = model_ctrl.copy()

    control_vars = [
        "riego_any",
        "riego_tecnificado_any",
        "usuario_agua",
        "uso_maquinaria",
        "semilla_certificada_any",
        "usa_abono",
        "usa_fertilizantes",
        "capacitacion_recibida",
        "asistencia_tecnica_recibida",
        "credito_obtenido",
        "asociacion_miembro",
    ]

    prevalence = (
        ctrl[control_vars]
        .apply(pd.to_numeric, errors="coerce")
        .mean()
        .sort_values(ascending=False)
    )
    prevalence

    fig, ax = plt.subplots(figsize=(7, 4))
    prevalence.plot(kind="bar", ax=ax, color="#4E79A7")
    ax.set_title("Control prevalence (mean of binary indicators)")
    ax.set_ylabel("share = 1")
    ax.set_ylim(0, max(0.05, prevalence.max() * 1.2))
    plt.tight_layout()
    if SAVE_PLOTS:
        fig.savefig(PLOT_DIR / "eda_controls_prevalence.png", dpi=150)

    riego_by_region = (
        ctrl.groupby("region_natural", dropna=False)["riego_any"].mean().reset_index()
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=riego_by_region, x="region_natural", y="riego_any", ax=ax, color="#59A14F")
    ax.set_title("Irrigation prevalence by region")
    ax.set_xlabel("region_natural")
    ax.set_ylabel("mean riego_any")
    ax.tick_params(axis="x", rotation=30)
    plt.tight_layout()
    if SAVE_PLOTS:
        fig.savefig(PLOT_DIR / "eda_irrigation_by_region.png", dpi=150)
else:
    print("Controls dataset not available; skipping controls analysis.")

# %% [markdown]
# ## Correlation scan (selected numeric variables)
#
# This is a quick diagnostic to see broad relationships among core metrics.

# %%
num_vars = [
    "log1p_valor_total",
    "log1p_area_total_ha",
    "log1p_input_costs",
    "log1p_labor_total",
    "diversificacion_area",
    "num_crops_area",
    "num_practices",
]

corr_df = model[num_vars].corr()

fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(corr_df, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
ax.set_title("Correlation matrix (selected variables)")
plt.tight_layout()
if SAVE_PLOTS:
    fig.savefig(PLOT_DIR / "eda_correlation_heatmap.png", dpi=150)

# %% [markdown]
# ## Interpretation
#
# - Diversification shows a pronounced mass at zero, consistent with monocrop
#   production (HHI = 1). This is visible in both the histogram and the monocrop
#   share diagnostic.
# - Output, input costs, and labor are heavily right-skewed; log transforms are
#   appropriate for modeling and visualization.
# - Practice adoption differs by region and size, suggesting heterogeneity that
#   could be captured with interactions or stratified models.
# - Control variables (irrigation, machinery, seed use, training/credit) display
#   varied prevalence; some are rare and may require careful handling in models.
# - Weighted vs unweighted means can diverge, indicating that expansion weights
#   matter for population-level inference.
#
# Next steps could include formal modeling of log output on diversification,
# inputs, labor, and controls, plus robustness checks by region and size.
