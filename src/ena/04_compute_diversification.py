#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(REPO_ROOT / "src"))

from features.diversification import compute_diversification


INTERMEDIATE_DIR = REPO_ROOT / "data" / "intermediate"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
OUTPUT_TABLES = REPO_ROOT / "outputs" / "tables"

ID_COLS = ["anio", "ccdd", "ccpp", "ccdi", "psu", "id_prod", "ua"]


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
    schema_path = INTERMEDIATE_DIR / "ena2024_schema.parquet"
    if not schema_path.exists():
        raise FileNotFoundError(f"Missing schema file: {schema_path}")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(schema_path)

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

    features_path = PROCESSED_DIR / "ena2024_features.parquet"
    features.to_parquet(features_path, index=False)

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

    summary_path_csv = OUTPUT_TABLES / "01_diversification_descriptives.csv"
    summary.to_csv(summary_path_csv, index=False)

    summary_path_md = OUTPUT_TABLES / "01_diversification_descriptives.md"
    summary_path_md.write_text(to_markdown(summary), encoding="utf-8")

    print(f"Wrote {features_path}")
    print(f"Wrote {summary_path_csv}")
    print(f"Wrote {summary_path_md}")


if __name__ == "__main__":
    sys.exit(main())
