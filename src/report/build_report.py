#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_TABLES = REPO_ROOT / "outputs" / "tables"
REPORTS_DIR = REPO_ROOT / "reports"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
INTERMEDIATE_DIR = REPO_ROOT / "data" / "intermediate"


def to_markdown(df: pd.DataFrame) -> str:
    try:
        return df.to_markdown(index=False)
    except Exception:
        cols = df.columns.tolist()
        lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
        for _, row in df.iterrows():
            lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
        return "\n".join(lines)


def git_hash() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT)
        return out.decode().strip()
    except Exception:
        return "unknown"


def main() -> None:
    OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    model_path = PROCESSED_DIR / "model_data_ena2024.parquet"
    model = pd.read_parquet(model_path)

    # Sample overview
    model["size_cat"] = model["size_cat"].astype("string")
    summary_frames = []
    summary_frames.append(model.assign(group_type="overall", group="overall"))
    summary_frames.append(model.assign(group_type="region", group=model["region_natural"].astype("string")))
    summary_frames.append(model.assign(group_type="size", group=model["size_cat"]))

    overview = (
        pd.concat(summary_frames, ignore_index=True)
        .groupby(["group_type", "group"], dropna=False)
        .agg(
            n=("id_prod", "count"),
            weight_sum=("weight", "sum"),
            mean_area_ha=("area_total_ha", "mean"),
            mean_valor_total=("valor_total", "mean"),
            mean_diversif=("diversificacion_area", "mean"),
            mean_practice_any=("practice_any", "mean"),
        )
        .reset_index()
    )
    overview_csv = OUTPUT_TABLES / "00_sample_overview.csv"
    overview_md = OUTPUT_TABLES / "00_sample_overview.md"
    overview.to_csv(overview_csv, index=False)
    overview_md.write_text(to_markdown(overview), encoding="utf-8")

    # Variable definitions table
    dict_df = pd.read_csv(INTERMEDIATE_DIR / "ena2024_dictionary.csv")
    dict_lookup = dict(zip(dict_df["variable"], dict_df["description"]))
    var_defs = [
        {
            "variable": "valor_total",
            "definition": "Sum of crop value components (P220_1_VAL, P220_2_VAL, P220_3A_VAL, P220_3B_VAL).",
            "notes": "Output for SFA.",
        },
        {
            "variable": "area_total_ha",
            "definition": dict_lookup.get("P217_SUP_ha", ""),
            "notes": "Sum of harvested area across crops.",
        },
        {
            "variable": "diversificacion_area",
            "definition": "1 - HHI based on harvested area shares.",
            "notes": "Main diversification index.",
        },
        {
            "variable": "hhi_area",
            "definition": "Sum of squared harvested area shares.",
            "notes": "HHI concentration index.",
        },
        {
            "variable": "shannon_area",
            "definition": "Shannon entropy using harvested area shares.",
            "notes": "Alternative diversification index.",
        },
        {
            "variable": "num_crops_area",
            "definition": "Count of distinct crops (P204_COD).",
            "notes": "Alternative diversification measure.",
        },
        {
            "variable": "labor_total",
            "definition": "Sum of permanent and seasonal workers (P1001A_2A_*C, P1001A_2B_*C).",
            "notes": "Labor input.",
        },
        {
            "variable": "input_costs",
            "definition": "Sum of expenditures on abono, fertilizantes, plaguicidas (P237_VAL, P239, P241).",
            "notes": "Intermediate input proxy.",
        },
        {
            "variable": "practice_any",
            "definition": "1 if any agricultural practice P301A_* equals 1.",
            "notes": "Sustainable practices outcome.",
        },
        {
            "variable": "size_cat",
            "definition": "Producer size categories based on area_total_ha.",
            "notes": "Small <2ha, Medium 2-5ha, Large >5ha.",
        },
        {
            "variable": "weight",
            "definition": dict_lookup.get("FACTOR_PRODUCTOR", ""),
            "notes": "Survey expansion weight.",
        },
        {
            "variable": "psu",
            "definition": dict_lookup.get("NSEGM", ""),
            "notes": "Primary sampling unit.",
        },
        {
            "variable": "estrato",
            "definition": dict_lookup.get("ESTRATO", ""),
            "notes": "Sampling stratum.",
        },
    ]
    var_defs_df = pd.DataFrame(var_defs)
    var_defs_csv = OUTPUT_TABLES / "99_variable_definitions_table.csv"
    var_defs_md = OUTPUT_TABLES / "99_variable_definitions_table.md"
    var_defs_df.to_csv(var_defs_csv, index=False)
    var_defs_md.write_text(to_markdown(var_defs_df), encoding="utf-8")

    # Build report
    report_path = REPORTS_DIR / "reporte_final.md"
    sections = []
    sections.append("# El rol de la diversificacion de cultivos en la productividad agropecuaria: El caso del Peru\n")
    sections.append("## Motivacion y preguntas\n")
    sections.append(
        "Se evalua la relacion entre diversificacion de cultivos y productividad/eficiencia (SFA), "
        "asi como su asociacion con practicas sostenibles (logit) usando ENA 2024."
    )
    sections.append("\n## Datos ENA 2024 y diseno muestral\n")
    sections.append("Fuente: ENA 2024 (INEI). Diseno muestral con pesos (FACTOR_PRODUCTOR), estratos y PSU.\n")
    sections.append("### Tabla 00. Resumen muestral\n")
    sections.append((OUTPUT_TABLES / "00_sample_overview.md").read_text(encoding="utf-8"))

    sections.append("\n## Indice de diversificacion (HHI)\n")
    sections.append((OUTPUT_TABLES / "01_diversification_descriptives.md").read_text(encoding="utf-8"))

    sections.append("\n## Resultados SFA\n")
    sections.append((OUTPUT_TABLES / "02_sfa_main.md").read_text(encoding="utf-8"))
    sections.append("\n### Robustez SFA\n")
    sections.append((OUTPUT_TABLES / "03_sfa_robustness.md").read_text(encoding="utf-8"))

    sections.append("\n## Resultados logit (practicas sostenibles)\n")
    sections.append((OUTPUT_TABLES / "04_logit_main.md").read_text(encoding="utf-8"))
    sections.append("\n### Robustez logit\n")
    sections.append((OUTPUT_TABLES / "05_logit_robustness.md").read_text(encoding="utf-8"))

    sections.append("\n## Definiciones de variables\n")
    sections.append((OUTPUT_TABLES / "99_variable_definitions_table.md").read_text(encoding="utf-8"))

    sections.append("\n## Limitaciones\n")
    sections.append("- SFA no usa pesos por limitaciones del paquete.\n")
    sections.append("- Algunas variables presentan faltantes; ver docs/DATA_GAPS.md.\n")

    report_path.write_text("\n".join(sections), encoding="utf-8")

    # Manifest
    manifest = {
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "git_hash": git_hash(),
        "n_obs_final": int(len(model)),
        "key_variables": [
            "valor_total",
            "area_total_ha",
            "labor_total",
            "input_costs",
            "diversificacion_area",
            "practice_any",
        ],
        "plans": {
            "output": "Plan A: P220_* value components from CAP200AB.",
            "land": "Plan A: P217_SUP_ha aggregated.",
            "labor": "Plan A: P1001A_2A/2B counts.",
            "inputs": "Plan A: P237_VAL + P239 + P241.",
            "practices": "Plan A: any P301A_* practice.",
        },
    }
    manifest_path = REPO_ROOT / "outputs" / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Wrote {overview_csv}")
    print(f"Wrote {var_defs_csv}")
    print(f"Wrote {report_path}")
    print(f"Wrote {manifest_path}")


if __name__ == "__main__":
    main()
