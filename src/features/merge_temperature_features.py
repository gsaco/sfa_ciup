#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
EXTERNAL_DIR = REPO_ROOT / "data" / "external" / "processed"
OUTPUT_TABLES = REPO_ROOT / "outputs" / "tables"


def build_ubigeo6(df: pd.DataFrame) -> pd.Series:
    ccdd = pd.to_numeric(df["ccdd"], errors="coerce").round().astype("Int64").astype("string").str.zfill(2)
    ccpp = pd.to_numeric(df["ccpp"], errors="coerce").round().astype("Int64").astype("string").str.zfill(2)
    ccdi = pd.to_numeric(df["ccdi"], errors="coerce").round().astype("Int64").astype("string").str.zfill(2)
    ubigeo6 = (ccdd + ccpp + ccdi).where(~(df["ccdd"].isna() | df["ccpp"].isna() | df["ccdi"].isna()))
    return ubigeo6


def to_markdown(df: pd.DataFrame) -> str:
    try:
        return df.to_markdown(index=False)
    except Exception:
        cols = df.columns.tolist()
        lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
        for _, row in df.iterrows():
            lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
        return "\n".join(lines)


def main() -> None:
    model_path = PROCESSED_DIR / "model_data_ena2024_plus_controls.parquet"
    temp_path = EXTERNAL_DIR / "temperature_district_features_2023_2024.parquet"

    if not model_path.exists():
        raise FileNotFoundError(f"Missing plus-controls data: {model_path}")
    if not temp_path.exists():
        raise FileNotFoundError(f"Missing temperature features: {temp_path}")

    OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)

    model = pd.read_parquet(model_path)
    model = model.copy()
    model["ubigeo6"] = build_ubigeo6(model)

    temp = pd.read_parquet(temp_path)

    merged = model.merge(temp, on="ubigeo6", how="left")

    out_parquet = PROCESSED_DIR / "model_data_ena2024_plus_controls_temp.parquet"
    out_csv = PROCESSED_DIR / "model_data_ena2024_plus_controls_temp.csv"
    merged.to_parquet(out_parquet, index=False)
    merged.to_csv(out_csv, index=False)

    temp_cols = ["tmean_2023", "tmean_2024", "delta_tmean_24_23"]
    topo_cols = ["elev_m", "slope_deg", "ruggedness"]

    summary_frames = []
    summary_frames.append(merged.assign(group_type="overall", group="overall"))
    summary_frames.append(merged.assign(group_type="region", group=merged["region_natural"].astype("string")))

    coverage = (
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

    if all(col in merged.columns for col in topo_cols):
        topo_cov = (
            pd.concat(summary_frames, ignore_index=True)
            .groupby(["group_type", "group"], dropna=False)
            .agg(
                share_topo_match=("elev_m", lambda x: x.notna().mean()),
                mean_elev_m=("elev_m", "mean"),
                mean_slope_deg=("slope_deg", "mean"),
                mean_ruggedness=("ruggedness", "mean"),
            )
            .reset_index()
        )
        coverage = coverage.merge(topo_cov, on=["group_type", "group"], how="left")

    coverage_csv = OUTPUT_TABLES / "12_temp_topo_coverage.csv"
    coverage_md = OUTPUT_TABLES / "12_temp_topo_coverage.md"
    coverage.to_csv(coverage_csv, index=False)
    coverage_md.write_text(to_markdown(coverage), encoding="utf-8")

    print(f"Wrote {out_parquet}")
    print(f"Wrote {coverage_csv}")


if __name__ == "__main__":
    main()
