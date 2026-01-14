#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns


REPO_ROOT = Path(__file__).resolve().parents[1]
PLOTS_DIR = REPO_ROOT / "outputs" / "plots"
SUBDIRS = {
    "index": PLOTS_DIR / "00_index",
    "quality": PLOTS_DIR / "01_data_quality",
    "geo": PLOTS_DIR / "02_geospatial",
    "models": PLOTS_DIR / "03_models",
}

KEY_COLS = ["anio", "ccdd", "ccpp", "ccdi", "psu", "id_prod", "ua"]


def ensure_dirs() -> None:
    for path in SUBDIRS.values():
        path.mkdir(parents=True, exist_ok=True)


def save_fig(fig: plt.Figure, path_base: Path) -> None:
    fig.tight_layout()
    fig.savefig(path_base.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(path_base.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


def normalize_keys(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    df = df.copy()
    for col in keys:
        if col in df.columns:
            df[col] = df[col].astype("string").str.replace(r"\.0$", "", regex=True)
    return df


def plot_log_valor_total(df: pd.DataFrame) -> None:
    sub = df[df["valor_total"] > 0].copy()
    sub["log_valor_total"] = np.log(sub["valor_total"])
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(sub["log_valor_total"], bins=50, kde=True, ax=ax, color="#4C78A8")
    ax.set_title("Log(valor_total) (solo valores positivos)")
    ax.set_xlabel("log(valor_total)")
    ax.set_ylabel("Count")
    ax.text(
        0.02,
        0.95,
        f"n={len(sub):,} (excluye valor_total <= 0)",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
    )
    save_fig(fig, SUBDIRS["quality"] / "hist_log_valor_total")


def plot_diversification_distributions(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    sns.histplot(df["diversificacion_area"], bins=40, kde=True, ax=axes[0], color="#59A14F")
    axes[0].set_title("Diversificacion (1 - HHI)")
    axes[0].set_xlabel("diversificacion_area")
    axes[0].set_ylabel("Count")

    sns.histplot(df["shannon_area"], bins=40, kde=True, ax=axes[1], color="#EDC949")
    axes[1].set_title("Shannon (area)")
    axes[1].set_xlabel("shannon_area")
    axes[1].set_ylabel("Count")

    sns.histplot(df["num_crops_area"], bins=30, kde=False, ax=axes[2], color="#9C755F")
    axes[2].set_title("Numero de cultivos (area)")
    axes[2].set_xlabel("num_crops_area")
    axes[2].set_ylabel("Count")

    save_fig(fig, SUBDIRS["quality"] / "diversification_distributions")


def plot_diversif_vs_num_crops(df: pd.DataFrame) -> None:
    sub = df.dropna(subset=["diversificacion_area", "num_crops_area"]).copy()
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(
        sub["diversificacion_area"],
        sub["num_crops_area"],
        alpha=0.2,
        s=10,
        color="#4C78A8",
        edgecolor="none",
    )
    ax.set_title("Diversificacion vs numero de cultivos")
    ax.set_xlabel("diversificacion_area")
    ax.set_ylabel("num_crops_area")
    save_fig(fig, SUBDIRS["quality"] / "diversif_vs_num_crops")


def plot_cost_diagnostic(series: pd.Series, label: str, filename: str) -> None:
    series = pd.to_numeric(series, errors="coerce").fillna(0)
    log1p_vals = np.log1p(series)
    p99 = series.quantile(0.99)
    vmax = series.max()
    share_zero = float((series == 0).mean())

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(log1p_vals, bins=50, ax=ax, color="#F28E2B")
    ax.axvline(np.log1p(p99), color="#E15759", linestyle="--", label=f"p99={p99:,.0f}")
    ax.axvline(np.log1p(vmax), color="#B07AA1", linestyle=":", label=f"max={vmax:,.0f}")
    ax.set_title(f"{label}: histograma log1p")
    ax.set_xlabel("log1p(valor)")
    ax.set_ylabel("Count")
    ax.text(
        0.02,
        0.95,
        f"share_zero={share_zero:.1%}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
    )
    ax.legend(fontsize=8)
    save_fig(fig, SUBDIRS["quality"] / filename)


def plot_practice_any_bars(df: pd.DataFrame) -> None:
    region = (
        df.groupby("region_natural")["practice_any"]
        .mean()
        .reset_index()
        .sort_values("region_natural")
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(region["region_natural"].astype(str), region["practice_any"], color="#59A14F")
    ax.set_title("Practice_any por region_natural")
    ax.set_xlabel("region_natural")
    ax.set_ylabel("Mean practice_any")
    save_fig(fig, SUBDIRS["quality"] / "practice_any_by_region")

    size = (
        df.groupby("size_cat")["practice_any"]
        .mean()
        .reset_index()
        .sort_values("size_cat")
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(size["size_cat"].astype(str), size["practice_any"], color="#4C78A8")
    ax.set_title("Practice_any por size_cat")
    ax.set_xlabel("size_cat")
    ax.set_ylabel("Mean practice_any")
    ax.tick_params(axis="x", rotation=20)
    save_fig(fig, SUBDIRS["quality"] / "practice_any_by_size")


def plot_num_practices_hist(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(df["num_practices"], bins=25, ax=ax, color="#76B7B2")
    ax.set_title("Distribucion de num_practices")
    ax.set_xlabel("num_practices")
    ax.set_ylabel("Count")
    save_fig(fig, SUBDIRS["quality"] / "num_practices_hist")


def plot_usuario_agua_heatmap(df: pd.DataFrame) -> None:
    ct = pd.crosstab(df["usuario_agua"], df["practice_any"], normalize="index")
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(ct, annot=True, fmt=".2f", cmap="YlGnBu", ax=ax)
    ax.set_title("Usuario_agua vs practice_any (row %)")
    ax.set_xlabel("practice_any")
    ax.set_ylabel("usuario_agua")
    save_fig(fig, SUBDIRS["quality"] / "usuario_agua_practice_any_heatmap")


def plot_map_points(df: pd.DataFrame, value_col: str, title: str, filename: str) -> None:
    sub = df.dropna(subset=["capital_lon", "capital_lat", value_col])
    fig, ax = plt.subplots(figsize=(6, 6))
    sc = ax.scatter(
        sub["capital_lon"],
        sub["capital_lat"],
        c=sub[value_col],
        cmap="viridis",
        s=12,
        alpha=0.85,
        edgecolor="none",
    )
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_xlim(-82, -68)
    ax.set_ylim(-19, 1)
    ax.set_aspect("equal", adjustable="box")
    fig.colorbar(sc, ax=ax, shrink=0.8)
    save_fig(fig, SUBDIRS["geo"] / filename)


def plot_coverage_map(df: pd.DataFrame) -> None:
    sub = df.dropna(subset=["capital_lon", "capital_lat"]).copy()
    layers = [
        ("prcp_total_z", "CHIRPS match"),
        ("tmean_2024", "Temperature match"),
        ("elev_m", "Topography match"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(14, 5), sharex=True, sharey=True)
    cmap = ListedColormap(["#E15759", "#59A14F"])
    for ax, (col, title) in zip(axes, layers):
        match = sub[col].notna().astype(int)
        ax.scatter(
            sub["capital_lon"],
            sub["capital_lat"],
            c=match,
            cmap=cmap,
            s=10,
            alpha=0.9,
            edgecolor="none",
        )
        ax.set_title(title)
        ax.set_xlabel("Longitude")
        ax.set_xlim(-82, -68)
        ax.set_ylim(-19, 1)
        ax.set_aspect("equal", adjustable="box")
    axes[0].set_ylabel("Latitude")
    save_fig(fig, SUBDIRS["geo"] / "map_external_coverage")


def plot_te_distributions(te_df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=te_df, x="size_cat", y="te", ax=ax, showfliers=False)
    ax.set_title("TE por size_cat")
    ax.set_xlabel("size_cat")
    ax.set_ylabel("TE")
    ax.tick_params(axis="x", rotation=20)
    save_fig(fig, SUBDIRS["models"] / "te_by_size_cat")

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=te_df, x="region_natural", y="te", ax=ax, showfliers=False)
    ax.set_title("TE por region_natural")
    ax.set_xlabel("region_natural")
    ax.set_ylabel("TE")
    save_fig(fig, SUBDIRS["models"] / "te_by_region")


def plot_te_vs_diversif(te_df: pd.DataFrame) -> None:
    df = te_df.dropna(subset=["diversificacion_area", "size_cat", "te"]).copy()
    bins = np.linspace(0, 1, 11)
    df["div_bin"] = pd.cut(df["diversificacion_area"], bins=bins, include_lowest=True)
    summary = (
        df.groupby(["size_cat", "div_bin"], dropna=False)
        .agg(te_mean=("te", "mean"), n=("te", "size"))
        .reset_index()
    )
    summary["div_mid"] = summary["div_bin"].apply(lambda x: (x.left + x.right) / 2)

    fig, ax = plt.subplots(figsize=(7, 4))
    for size_cat, sdf in summary.groupby("size_cat"):
        sdf = sdf.sort_values("div_mid")
        ax.plot(sdf["div_mid"], sdf["te_mean"], marker="o", label=str(size_cat))
    ax.set_title("TE vs diversificacion (bins)")
    ax.set_xlabel("diversificacion_area (bin mid)")
    ax.set_ylabel("Mean TE")
    ax.legend(fontsize=8)
    save_fig(fig, SUBDIRS["models"] / "te_vs_diversif_binned")


def load_logit_coeffs(path: Path, model_name: str) -> dict[str, float]:
    df = pd.read_csv(path)
    df = df[df["model"] == model_name]
    return dict(zip(df["term"], df["estimate"]))


def predict_logit(df: pd.DataFrame, coef: dict[str, float]) -> pd.Series:
    base = pd.Series(0.0, index=df.index)
    base += coef.get("(Intercept)", 0.0)
    base += coef.get("diversificacion_area", 0.0) * df["diversificacion_area"]
    base += coef.get("log_area", 0.0) * df["log_area"]

    base += coef.get("size_catmediano_2_5ha", 0.0) * (df["size_cat"] == "mediano_2_5ha").astype(int)
    base += coef.get("size_catpequeno_<2ha", 0.0) * (df["size_cat"] == "pequeno_<2ha").astype(int)

    base += coef.get("region_natural2", 0.0) * (df["region_natural"] == 2).astype(int)
    base += coef.get("region_natural3", 0.0) * (df["region_natural"] == 3).astype(int)

    base += coef.get(
        "diversificacion_area:size_catmediano_2_5ha", 0.0
    ) * df["diversificacion_area"] * (df["size_cat"] == "mediano_2_5ha").astype(int)
    base += coef.get(
        "diversificacion_area:size_catpequeno_<2ha", 0.0
    ) * df["diversificacion_area"] * (df["size_cat"] == "pequeno_<2ha").astype(int)

    return 1 / (1 + np.exp(-base))


def plot_logit_predictions(df: pd.DataFrame, coef: dict[str, float], title: str, filename: str) -> None:
    sub = df.dropna(subset=["diversificacion_area", "size_cat", "region_natural", "area_total_ha"]).copy()
    sub["log_area"] = np.log(sub["area_total_ha"] + 1)
    sub["pred_prob"] = predict_logit(sub, coef)

    bins = np.linspace(0, 1, 11)
    sub["div_bin"] = pd.cut(sub["diversificacion_area"], bins=bins, include_lowest=True)

    def weighted_mean(series: pd.Series, weights: pd.Series) -> float:
        if weights.isna().all():
            return float(series.mean())
        w = weights.fillna(0)
        if w.sum() == 0:
            return float(series.mean())
        return float((series * w).sum() / w.sum())

    summary_rows = []
    for (size_cat, div_bin), gdf in sub.groupby(["size_cat", "div_bin"], dropna=False):
        summary_rows.append(
            {
                "size_cat": size_cat,
                "div_bin": div_bin,
                "div_mid": (div_bin.left + div_bin.right) / 2,
                "pred_prob": weighted_mean(gdf["pred_prob"], gdf.get("weight", pd.Series(index=gdf.index))),
            }
        )
    summary = pd.DataFrame(summary_rows)

    fig, ax = plt.subplots(figsize=(7, 4))
    for size_cat, sdf in summary.groupby("size_cat"):
        sdf = sdf.sort_values("div_mid")
        ax.plot(sdf["div_mid"], sdf["pred_prob"], marker="o", label=str(size_cat))
    ax.set_title(title)
    ax.set_xlabel("diversificacion_area (bin mid)")
    ax.set_ylabel("Predicted probability")
    ax.set_ylim(0, 1)
    ax.legend(fontsize=8)
    save_fig(fig, SUBDIRS["models"] / filename)


def main() -> None:
    ensure_dirs()
    sns.set_theme(style="whitegrid")

    base = pd.read_parquet(REPO_ROOT / "data" / "processed" / "model_data_ena2024.parquet")
    controls = pd.read_parquet(REPO_ROOT / "data" / "processed" / "model_data_ena2024_plus_controls.parquet")
    geo = pd.read_parquet(REPO_ROOT / "data" / "processed" / "model_data_ena2024_plus_geo.parquet")
    geo2 = pd.read_parquet(REPO_ROOT / "data" / "processed" / "model_data_ena2024_plus_geo2.parquet")

    plot_log_valor_total(base)
    plot_diversification_distributions(base)
    plot_diversif_vs_num_crops(base)

    plot_cost_diagnostic(base["input_costs"], "input_costs", "cost_input_costs_log1p")
    plot_cost_diagnostic(controls["gasto_agua_riego"], "gasto_agua_riego", "cost_irrigation_cost_log1p")
    plot_cost_diagnostic(controls["gasto_semilla"], "gasto_semilla", "cost_seed_log1p")
    capital_total = (
        pd.to_numeric(controls["gasto_compra_maquinaria"], errors="coerce").fillna(0)
        + pd.to_numeric(controls["gasto_compra_equipos"], errors="coerce").fillna(0)
        + pd.to_numeric(controls["gasto_alquiler_mant_equipos"], errors="coerce").fillna(0)
    )
    plot_cost_diagnostic(capital_total, "capital_total", "cost_capital_log1p")

    plot_practice_any_bars(base)
    plot_num_practices_hist(base)
    plot_usuario_agua_heatmap(controls)

    plot_map_points(geo, "prcp_total_z", "CHIRPS prcp_total_z", "map_prcp_total_z")
    plot_map_points(geo2, "tmean_2024", "Temperature mean 2024", "map_tmean_2024")
    plot_map_points(geo2, "elev_m", "Elevation (m)", "map_elev_m")
    plot_coverage_map(geo2)

    te_path = REPO_ROOT / "data" / "processed" / "ena2024_with_TE.parquet"
    if te_path.exists():
        te = pd.read_parquet(te_path)
        base_norm = normalize_keys(base, KEY_COLS)
        te_norm = normalize_keys(te, KEY_COLS)
        merged = base_norm.merge(te_norm, on=KEY_COLS, how="inner")
        plot_te_distributions(merged)
        plot_te_vs_diversif(merged)

    logit_main_coef = load_logit_coeffs(REPO_ROOT / "outputs" / "tables" / "04_logit_main.csv", "main")
    plot_logit_predictions(base, logit_main_coef, "Predicted P(practice_any) vs diversificacion", "logit_pred_practice_any")

    robust_path = REPO_ROOT / "outputs" / "tables" / "05_logit_robustness.csv"
    if robust_path.exists():
        logit_two_plus_coef = load_logit_coeffs(robust_path, "alt_outcome_two_plus")
        plot_logit_predictions(
            base,
            logit_two_plus_coef,
            "Predicted P(practice_two_plus) vs diversificacion",
            "logit_pred_practice_two_plus",
        )


if __name__ == "__main__":
    main()
