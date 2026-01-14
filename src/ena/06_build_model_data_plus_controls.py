#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(REPO_ROOT / "src"))

from features.ena_controls import (
    extension_credit_education_features,
    fertilizer_seed_features,
    irrigation_features,
    machinery_capital_features,
)


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


def normalize_key_series(series: pd.Series) -> pd.Series:
    series = series.astype("string")
    return series.str.replace(r"\.0$", "", regex=True)


def main() -> None:
    base_path = PROCESSED_DIR / "model_data_ena2024.parquet"
    if not base_path.exists():
        raise FileNotFoundError(f"Missing base model data: {base_path}")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)

    base = pd.read_parquet(base_path)
    for col in ID_COLS:
        if col in base.columns:
            base[col] = normalize_key_series(base[col])

    controls_frames = [
        irrigation_features(),
        machinery_capital_features(),
        fertilizer_seed_features(),
        extension_credit_education_features(),
    ]

    merged = base.copy()
    for controls in controls_frames:
        for col in ID_COLS:
            if col in controls.columns:
                controls[col] = normalize_key_series(controls[col])
        merged = merged.merge(controls, on=ID_COLS, how="left")

    output_parquet = PROCESSED_DIR / "model_data_ena2024_plus_controls.parquet"
    output_csv = PROCESSED_DIR / "model_data_ena2024_plus_controls.csv"
    merged.to_parquet(output_parquet, index=False)
    merged.to_csv(output_csv, index=False)

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

    missing_controls = [col for col in control_cols if col not in merged.columns]
    if missing_controls:
        raise ValueError(f"Missing control columns in merged data: {missing_controls}")

    coverage = summarize_controls(merged, control_cols)
    coverage_csv = OUTPUT_TABLES / "11_controls_ena_coverage.csv"
    coverage_md = OUTPUT_TABLES / "11_controls_ena_coverage.md"
    coverage.to_csv(coverage_csv, index=False)
    coverage_md.write_text(to_markdown(coverage), encoding="utf-8")

    print(f"Wrote {output_parquet}")
    print(f"Wrote {output_csv}")
    print(f"Wrote {coverage_csv}")


if __name__ == "__main__":
    sys.exit(main())
