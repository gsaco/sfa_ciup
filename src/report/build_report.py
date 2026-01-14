#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_TABLES = REPO_ROOT / "outputs" / "tables"
REPORTS_DIR = REPO_ROOT / "reports"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
INTERMEDIATE_DIR = REPO_ROOT / "data" / "intermediate"
EXTERNAL_RAW = REPO_ROOT / "data" / "external" / "raw"
EXTERNAL_PROCESSED = REPO_ROOT / "data" / "external" / "processed"


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


def r_version() -> str:
    try:
        out = subprocess.check_output(["Rscript", "-e", "cat(R.version.string)"], cwd=REPO_ROOT)
        return out.decode().strip()
    except Exception:
        return "unknown"


def sha256(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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

    # External data section
    sections.append("\n## Mejoras con datos externos (UBIGEO + CHIRPS)\n")
    sections.append(
        "Se incorporaron coordenadas y area distrital, y precipitacion CHIRPS como control exogeno. "
        "Las tablas siguientes comparan resultados base vs controles geo/clima."
    )
    if (OUTPUT_TABLES / "06_geo_feature_coverage.md").exists():
        sections.append("\n### Tabla 06. Cobertura geo/clima\n")
        sections.append((OUTPUT_TABLES / "06_geo_feature_coverage.md").read_text(encoding="utf-8"))
    if (OUTPUT_TABLES / "07_sfa_with_geo_controls.md").exists():
        sections.append("\n### Tabla 07. SFA con controles geo/clima\n")
        sections.append((OUTPUT_TABLES / "07_sfa_with_geo_controls.md").read_text(encoding="utf-8"))
    if (OUTPUT_TABLES / "08_sfa_compare_main_effects.md").exists():
        sections.append("\n### Tabla 08. Comparacion efectos SFA\n")
        sections.append((OUTPUT_TABLES / "08_sfa_compare_main_effects.md").read_text(encoding="utf-8"))
    if (OUTPUT_TABLES / "09_logit_with_geo_controls.md").exists():
        sections.append("\n### Tabla 09. Logit con controles geo/clima\n")
        sections.append((OUTPUT_TABLES / "09_logit_with_geo_controls.md").read_text(encoding="utf-8"))
    if (OUTPUT_TABLES / "10_logit_compare_main_effects.md").exists():
        sections.append("\n### Tabla 10. Comparacion efectos logit\n")
        sections.append((OUTPUT_TABLES / "10_logit_compare_main_effects.md").read_text(encoding="utf-8"))

    sections.append("\n## Controles ENA adicionales\n")
    sections.append(
        "Se incorporan controles de capital, riego, semillas, asistencia tecnica, credito y educacion. "
        "Las tablas siguientes muestran cobertura y efectos econometricos."
    )
    if (OUTPUT_TABLES / "11_controls_ena_coverage.md").exists():
        sections.append("\n### Tabla 11. Cobertura controles ENA\n")
        sections.append((OUTPUT_TABLES / "11_controls_ena_coverage.md").read_text(encoding="utf-8"))
    if (OUTPUT_TABLES / "13_sfa_with_controls_ena.md").exists():
        sections.append("\n### Tabla 13. SFA con controles ENA\n")
        sections.append((OUTPUT_TABLES / "13_sfa_with_controls_ena.md").read_text(encoding="utf-8"))
    if (OUTPUT_TABLES / "16_logit_with_controls_ena.md").exists():
        sections.append("\n### Tabla 16. Logit con controles ENA\n")
        sections.append((OUTPUT_TABLES / "16_logit_with_controls_ena.md").read_text(encoding="utf-8"))

    sections.append("\n## Temperatura 2023-2024 y topografia\n")
    sections.append(
        "Se agregan controles exogenos de temperatura (2023-2024) y topografia a nivel distrital."
    )
    if (OUTPUT_TABLES / "12_temp_topo_coverage.md").exists():
        sections.append("\n### Tabla 12. Cobertura temperatura/topografia\n")
        sections.append((OUTPUT_TABLES / "12_temp_topo_coverage.md").read_text(encoding="utf-8"))
    if (OUTPUT_TABLES / "14_sfa_with_temp_topo.md").exists():
        sections.append("\n### Tabla 14. SFA con temperatura/topografia\n")
        sections.append((OUTPUT_TABLES / "14_sfa_with_temp_topo.md").read_text(encoding="utf-8"))
    if (OUTPUT_TABLES / "17_logit_with_temp_topo.md").exists():
        sections.append("\n### Tabla 17. Logit con temperatura/topografia\n")
        sections.append((OUTPUT_TABLES / "17_logit_with_temp_topo.md").read_text(encoding="utf-8"))

    sections.append("\n## Comparaciones de robustez (controles + geo/clima)\n")
    sections.append(
        "Se comparan los coeficientes de diversificacion e interacciones en las especificaciones "
        "baseline, con controles ENA y con temperatura/topografia."
    )
    if (OUTPUT_TABLES / "15_sfa_compare_effects_all.md").exists():
        sections.append("\n### Tabla 15. Comparacion efectos SFA\n")
        sections.append((OUTPUT_TABLES / "15_sfa_compare_effects_all.md").read_text(encoding="utf-8"))
    if (OUTPUT_TABLES / "18_logit_compare_effects_all.md").exists():
        sections.append("\n### Tabla 18. Comparacion efectos logit\n")
        sections.append((OUTPUT_TABLES / "18_logit_compare_effects_all.md").read_text(encoding="utf-8"))
    if (OUTPUT_TABLES / "sample_loss_analysis.md").exists():
        sections.append("\n### Analisis de perdida muestral\n")
        sections.append((OUTPUT_TABLES / "sample_loss_analysis.md").read_text(encoding="utf-8"))

    sections.append("\n## Definiciones de variables\n")
    sections.append((OUTPUT_TABLES / "99_variable_definitions_table.md").read_text(encoding="utf-8"))

    sections.append("\n## Limitaciones\n")
    sections.append("- SFA no usa pesos por limitaciones del paquete.\n")
    sections.append("- Algunas variables presentan faltantes; ver docs/DATA_GAPS.md.\n")

    report_path.write_text("\n".join(sections), encoding="utf-8")

    # External metadata
    ubigeo_plan = "unknown"
    ubigeo_plan_path = EXTERNAL_PROCESSED / "ubigeo_plan_used.json"
    if ubigeo_plan_path.exists():
        ubigeo_plan = json.loads(ubigeo_plan_path.read_text(encoding="utf-8")).get("plan_used", "unknown")

    chirps_meta = {}
    chirps_meta_path = EXTERNAL_RAW / "chirps" / "metadata.json"
    if chirps_meta_path.exists():
        chirps_meta = json.loads(chirps_meta_path.read_text(encoding="utf-8"))

    temp_meta = {}
    temp_meta_path = EXTERNAL_RAW / "temperature" / "metadata.json"
    if temp_meta_path.exists():
        temp_meta = json.loads(temp_meta_path.read_text(encoding="utf-8"))

    topo_meta = {}
    topo_meta_path = EXTERNAL_RAW / "topography" / "metadata.json"
    if topo_meta_path.exists():
        topo_meta = json.loads(topo_meta_path.read_text(encoding="utf-8"))

    plus_geo_path = PROCESSED_DIR / "model_data_ena2024_plus_geo.parquet"
    geo_match_rate = None
    chirps_match_rate = None
    if plus_geo_path.exists():
        geo = pd.read_parquet(plus_geo_path)
        geo_match_rate = float(geo["capital_lat"].notna().mean())
        chirps_match_rate = float(geo["prcp_2024_total"].notna().mean())

    plus_controls_path = PROCESSED_DIR / "model_data_ena2024_plus_controls.parquet"
    plus_controls_temp_path = PROCESSED_DIR / "model_data_ena2024_plus_controls_temp.parquet"
    plus_geo2_path = PROCESSED_DIR / "model_data_ena2024_plus_geo2.parquet"

    n_obs_controls = None
    n_obs_controls_temp = None
    n_obs_geo2 = None

    controls = None
    if plus_controls_path.exists():
        controls = pd.read_parquet(plus_controls_path)
        n_obs_controls = int(len(controls))

    if plus_controls_temp_path.exists():
        n_obs_controls_temp = int(len(pd.read_parquet(plus_controls_temp_path)))

    geo2 = None
    if plus_geo2_path.exists():
        geo2 = pd.read_parquet(plus_geo2_path)
        n_obs_geo2 = int(len(geo2))

    temp_match_rate = None
    topo_match_rate = None
    if geo2 is not None:
        if "tmean_2024" in geo2.columns:
            temp_match_rate = float(geo2["tmean_2024"].notna().mean())
        if "elev_m" in geo2.columns:
            topo_match_rate = float(geo2["elev_m"].notna().mean())

    controls_coverage = {}
    if controls is not None:
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
        for col in control_cols:
            if col in controls.columns:
                controls_coverage[col] = float(controls[col].notna().mean())

    output_tables_csv = sorted(
        [path.relative_to(REPO_ROOT).as_posix() for path in OUTPUT_TABLES.glob("*.csv")]
    )
    output_tables_md = sorted(
        [path.relative_to(REPO_ROOT).as_posix() for path in OUTPUT_TABLES.glob("*.md")]
    )

    data_outputs = []
    for path in [model_path, plus_controls_path, plus_controls_temp_path, plus_geo2_path, plus_geo_path]:
        if path.exists():
            data_outputs.append(path.relative_to(REPO_ROOT).as_posix())

    key_hashes = {}
    for path in [
        OUTPUT_TABLES / "02_sfa_main.csv",
        OUTPUT_TABLES / "04_logit_main.csv",
        OUTPUT_TABLES / "11_controls_ena_coverage.csv",
        OUTPUT_TABLES / "12_temp_topo_coverage.csv",
        OUTPUT_TABLES / "13_sfa_with_controls_ena.csv",
        OUTPUT_TABLES / "14_sfa_with_temp_topo.csv",
        OUTPUT_TABLES / "15_sfa_compare_effects_all.csv",
        OUTPUT_TABLES / "16_logit_with_controls_ena.csv",
        OUTPUT_TABLES / "17_logit_with_temp_topo.csv",
        OUTPUT_TABLES / "18_logit_compare_effects_all.csv",
        OUTPUT_TABLES / "sample_loss_analysis.csv",
    ]:
        if path.exists():
            key_hashes[path.relative_to(REPO_ROOT).as_posix()] = sha256(path)

    # Manifest
    external_hashes = {}
    for path in [
        EXTERNAL_RAW / "ubigeo" / "DD_TB_UBIGEOS.xlsx",
        EXTERNAL_RAW / "ubigeo" / "ubigeo_distrito.csv",
        EXTERNAL_RAW / "chirps" / "metadata.json",
        EXTERNAL_RAW / "temperature" / "metadata.json",
        EXTERNAL_RAW / "topography" / "metadata.json",
    ]:
        if path.exists():
            external_hashes[path.as_posix()] = sha256(path)

    manifest = {
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "git_hash": git_hash(),
        "versions": {
            "python": sys.version.split()[0],
            "pandas": pd.__version__,
            "r": r_version(),
        },
        "n_obs_final": int(len(model)),
        "n_obs_controls": n_obs_controls,
        "n_obs_controls_temp": n_obs_controls_temp,
        "n_obs_geo2": n_obs_geo2,
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
            "ubigeo_plan": ubigeo_plan,
            "chirps_plan": chirps_meta.get("plan_used", "unknown"),
            "chirps_baseline_start": chirps_meta.get("baseline_start"),
            "chirps_baseline_end": chirps_meta.get("baseline_end"),
        },
        "geo_match_rate": geo_match_rate,
        "chirps_match_rate": chirps_match_rate,
        "temp_match_rate": temp_match_rate,
        "topo_match_rate": topo_match_rate,
        "controls_coverage": controls_coverage,
        "output_tables_csv": output_tables_csv,
        "output_tables_md": output_tables_md,
        "data_outputs": data_outputs,
        "key_hashes": key_hashes,
        "external_hashes": external_hashes,
        "temperature_source": temp_meta.get("source"),
        "temperature_accessed": temp_meta.get("accessed"),
        "topography_source": topo_meta.get("source"),
        "topography_accessed": topo_meta.get("accessed"),
    }
    manifest_path = REPO_ROOT / "outputs" / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Wrote {overview_csv}")
    print(f"Wrote {var_defs_csv}")
    print(f"Wrote {report_path}")
    print(f"Wrote {manifest_path}")


if __name__ == "__main__":
    main()
