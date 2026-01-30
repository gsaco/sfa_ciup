#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
OUTPUT_TABLES = REPO_ROOT / "outputs" / "tables"


def to_markdown(df: pd.DataFrame) -> str:
    try:
        return df.to_markdown(index=False)
    except Exception:
        cols = df.columns.tolist()
        lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
        for _, row in df.iterrows():
            lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
        return "\n".join(lines)


def build_rows(base: pd.DataFrame, geo: pd.DataFrame, sample_type: str, weight_col: str | None) -> list[dict[str, object]]:
    rows = []
    group_specs = [("overall", None), ("region", "region_natural"), ("size", "size_cat")]

    for group_type, group_col in group_specs:
        if group_col is None:
            base_groups = [("overall", base)]
            geo_groups = {("overall"): geo}
        else:
            base_groups = list(base.groupby(group_col, dropna=False))
            geo_groups = {g: df for g, df in geo.groupby(group_col, dropna=False)}

        for group, bdf in base_groups:
            gdf = geo_groups.get(group, geo.iloc[0:0])
            n_base = len(bdf)
            n_geo = len(gdf)
            weight_base = float(bdf[weight_col].sum()) if weight_col and weight_col in bdf.columns else float("nan")
            weight_geo = float(gdf[weight_col].sum()) if weight_col and weight_col in gdf.columns else float("nan")
            share_remaining = (n_geo / n_base) if n_base > 0 else float("nan")
            rows.append(
                {
                    "sample_type": sample_type,
                    "group_type": group_type,
                    "group": group,
                    "n_base": n_base,
                    "n_geo2": n_geo,
                    "share_remaining": share_remaining,
                    "weight_base": weight_base,
                    "weight_geo2": weight_geo,
                }
            )

    return rows


def required_non_missing(df: pd.DataFrame, columns: list[str]) -> pd.Series:
    cols = [col for col in columns if col in df.columns]
    if not cols:
        return pd.Series([True] * len(df), index=df.index)
    return df[cols].notna().all(axis=1)


def read_parquet_with_fallback(path: Path) -> pd.DataFrame:
    try:
        return pd.read_parquet(path)
    except Exception as exc:
        csv_path = path.with_suffix(".csv")
        if not csv_path.exists():
            raise
        print(f"Warning: failed to read {path} ({exc}); using {csv_path} instead.")
        return pd.read_csv(csv_path)


def resolve_input_cost_col(df: pd.DataFrame) -> str:
    for col in ["costo_total_agropecuario", "gasto_agricola_total", "input_costs"]:
        if col in df.columns:
            return col
    return "input_costs"


def main() -> None:
    base_path = PROCESSED_DIR / "model_data_ena2024.parquet"
    geo_path = PROCESSED_DIR / "model_data_ena2024_plus_geo2.parquet"
    if not base_path.exists() or not geo_path.exists():
        raise FileNotFoundError("Missing baseline or geo2 dataset for sample loss analysis")

    OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)

    base = read_parquet_with_fallback(base_path)
    geo = read_parquet_with_fallback(geo_path)

    # Logit sample: match R/02_logit_practices.R (model variables + survey design)
    logit_required = [
        "practice_any",
        "diversificacion_area",
        "weight",
        "area_total_ha",
        "size_cat",
        "region_natural",
        "psu",
        "estrato",
    ]
    base_logit = base[required_non_missing(base, logit_required)]

    geo_logit_required = logit_required + [
        "tmean_2024",
        "delta_tmean_24_23",
        "elev_m",
        "slope_deg",
        "ruggedness",
        "prcp_total_z",
    ]
    geo_logit = geo[required_non_missing(geo, geo_logit_required)]

    # SFA sample: match R/01_sfa_main.R (positive outputs, constructed inputs, plus climate/topo)
    base_input_col = resolve_input_cost_col(base)
    geo_input_col = resolve_input_cost_col(geo)

    base_sfa_required = [
        "valor_total",
        "area_total_ha",
        "labor_total",
        base_input_col,
        "diversificacion_area",
        "size_cat",
        "region_natural",
    ]
    base_sfa = base[
        (base["valor_total"] > 0)
        & (base["area_total_ha"] > 0)
        & required_non_missing(base, base_sfa_required)
    ]

    geo_sfa_required = [
        "valor_total",
        "area_total_ha",
        "labor_total",
        geo_input_col,
        "diversificacion_area",
        "size_cat",
        "region_natural",
    ] + [
        "tmean_2024",
        "delta_tmean_24_23",
        "slope_deg",
        "ruggedness",
        "prcp_total_z",
    ]
    if "surface_km2" in geo.columns:
        geo_sfa_required.append("surface_km2")
    geo_sfa = geo[
        (geo["valor_total"] > 0)
        & (geo["area_total_ha"] > 0)
        & required_non_missing(geo, geo_sfa_required)
    ]

    rows = []
    rows.extend(build_rows(base_logit, geo_logit, "logit", "weight"))
    rows.extend(build_rows(base_sfa, geo_sfa, "sfa", None))

    out = pd.DataFrame(rows)
    out_csv = OUTPUT_TABLES / "sample_loss_analysis.csv"
    out_md = OUTPUT_TABLES / "sample_loss_analysis.md"
    out.to_csv(out_csv, index=False)
    out_md.write_text(to_markdown(out), encoding="utf-8")

    print(f"Wrote {out_csv}")


if __name__ == "__main__":
    main()
