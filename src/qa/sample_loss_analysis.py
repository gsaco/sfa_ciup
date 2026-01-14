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


def main() -> None:
    base_path = PROCESSED_DIR / "model_data_ena2024.parquet"
    geo_path = PROCESSED_DIR / "model_data_ena2024_plus_geo2.parquet"
    if not base_path.exists() or not geo_path.exists():
        raise FileNotFoundError("Missing baseline or geo2 dataset for sample loss analysis")

    OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)

    base = pd.read_parquet(base_path)
    geo = pd.read_parquet(geo_path)

    # Logit sample: practice_any/diversificacion/weight
    base_logit = base[base["practice_any"].notna() & base["diversificacion_area"].notna() & base["weight"].notna()]
    geo_logit = geo[
        geo["practice_any"].notna()
        & geo["diversificacion_area"].notna()
        & geo["weight"].notna()
        & geo["tmean_2024"].notna()
        & geo["elev_m"].notna()
    ]

    # SFA sample: positive output and inputs, plus temp/topo
    base_sfa = base[
        (base["valor_total"] > 0)
        & (base["area_total_ha"] > 0)
        & base["diversificacion_area"].notna()
        & base["size_cat"].notna()
        & base["region_natural"].notna()
    ]
    geo_sfa = geo[
        (geo["valor_total"] > 0)
        & (geo["area_total_ha"] > 0)
        & geo["diversificacion_area"].notna()
        & geo["size_cat"].notna()
        & geo["region_natural"].notna()
        & geo["tmean_2024"].notna()
        & geo["elev_m"].notna()
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
