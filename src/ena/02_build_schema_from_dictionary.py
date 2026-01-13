#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

import pandas as pd
import pdfplumber


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
INTERMEDIATE_DIR = DATA_DIR / "intermediate"
DOCS_DIR = REPO_ROOT / "docs"
DICT_PATH = REPO_ROOT / "DICCIONARIO DE DATOS ENA-2024.pdf"


def normalize_text(text: str) -> str:
    return " ".join(text.replace("\n", " ").split())


def normalize_var(text: str) -> str:
    cleaned = text.replace("\n", "").replace(" ", "")
    cleaned = cleaned.replace("-", "")
    return cleaned.strip()


def infer_unit(description: str) -> str:
    desc = description.lower()
    if "hect" in desc:
        return "ha"
    if re.search(r"\bS/|\bSoles\b", description, flags=re.IGNORECASE):
        return "S/"
    if "kilogram" in desc or "kg" in desc:
        return "kg"
    if "año" in desc or "anio" in desc:
        return "year"
    return ""


def extract_dictionary(pdf_path: Path) -> pd.DataFrame:
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables() or []
            for table in tables:
                if not table or len(table) < 2:
                    continue
                for row in table[1:]:
                    if not row or len(row) < 3:
                        continue
                    var = normalize_var((row[1] or "").strip())
                    desc = (row[2] or "").strip()
                    if not var:
                        continue
                    rows.append(
                        {
                            "variable": var,
                            "description": normalize_text(desc),
                            "type": (row[4] or "").strip() if len(row) > 4 else "",
                            "length": (row[5] or "").strip() if len(row) > 5 else "",
                            "decimal": (row[6] or "").strip() if len(row) > 6 else "",
                            "page": page_idx,
                        }
                    )
    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("No dictionary entries extracted from PDF.")
    df = df.drop_duplicates(subset=["variable"], keep="first").reset_index(drop=True)
    return df


def build_schema_map() -> list[dict[str, str]]:
    return [
        {"raw": "ANIO", "std": "anio", "notes": "Survey year."},
        {"raw": "CCDD", "std": "ccdd", "notes": "Department code."},
        {"raw": "NOMBREDD", "std": "departamento", "notes": "Department name."},
        {"raw": "CCPP", "std": "ccpp", "notes": "Province code."},
        {"raw": "NOMBREPV", "std": "provincia", "notes": "Province name."},
        {"raw": "CCDI", "std": "ccdi", "notes": "District code."},
        {"raw": "NOMBREDI", "std": "distrito", "notes": "District name."},
        {"raw": "NSEGM", "std": "psu", "notes": "Primary sampling unit (segment)."},
        {"raw": "ID_PROD", "std": "id_prod", "notes": "Producer identifier."},
        {"raw": "UA", "std": "ua", "notes": "Agricultural unit."},
        {"raw": "REGION", "std": "region_natural", "notes": "Natural region."},
        {"raw": "ESTRATO", "std": "estrato", "notes": "Sampling stratum."},
        {"raw": "FACTOR_PRODUCTOR", "std": "weight", "notes": "Expansion weight for producer."},
        {"raw": "LATITUD", "std": "latitud", "notes": "Latitude."},
        {"raw": "LONGITUD", "std": "longitud", "notes": "Longitude."},
        {"raw": "P204_COD", "std": "crop_code", "notes": "Crop code."},
        {"raw": "P204_NOM", "std": "crop_name", "notes": "Crop name."},
        {"raw": "P217_SUP_ha", "std": "area_cosechada_ha", "notes": "Harvested area by crop."},
        {"raw": "P219_CANT_1", "std": "produccion_cant_ent", "notes": "Production quantity (integer)."},
        {"raw": "P219_CANT_2", "std": "produccion_cant_dec", "notes": "Production quantity (decimal)."},
        {"raw": "P220_1_VAL", "std": "valor_venta", "notes": "Value sold."},
        {"raw": "P220_2_VAL", "std": "valor_consumo", "notes": "Value for household consumption."},
        {"raw": "P220_3A_VAL", "std": "valor_semilla_autoconsumo", "notes": "Value for seed (auto-consumption)."},
        {"raw": "P220_3B_VAL", "std": "valor_semilla_venta", "notes": "Value for seed (sold)."},
        {"raw": "P1001A_TOTAL", "std": "gasto_agricola_total", "notes": "Total agricultural expenses."},
        {"raw": "P1000_TOTAL", "std": "costo_total_agropecuario", "notes": "Total agricultural + livestock cost."},
        {"raw": "P1001A_2A_1C", "std": "jornaleros_perm_h", "notes": "Permanent workers (men)."},
        {"raw": "P1001A_2A_2C", "std": "jornaleros_perm_m", "notes": "Permanent workers (women)."},
        {"raw": "P1001A_2B_1C", "std": "jornaleros_event_h", "notes": "Seasonal workers (men)."},
        {"raw": "P1001A_2B_2C", "std": "jornaleros_event_m", "notes": "Seasonal workers (women)."},
        {"raw": "P237_VAL", "std": "gasto_abono", "notes": "Expenditure on organic fertilizer."},
        {"raw": "P239", "std": "gasto_fertilizantes", "notes": "Expenditure on fertilizers."},
        {"raw": "P241", "std": "gasto_plaguicidas", "notes": "Expenditure on pesticides."},
        {"raw": "P301A_1", "std": "practica_analisis_suelos", "notes": "Agricultural practice."},
        {"raw": "P301A_2", "std": "practica_materia_organica", "notes": "Agricultural practice."},
        {"raw": "P301A_3", "std": "practica_rotacion_cultivos", "notes": "Agricultural practice."},
        {"raw": "P301A_4", "std": "practica_terrazas_zanjas", "notes": "Agricultural practice."},
        {"raw": "P301A_4A", "std": "practica_recuperacion_erosion", "notes": "Agricultural practice."},
        {"raw": "P301A_4B", "std": "practica_recuperacion_compactacion", "notes": "Agricultural practice."},
        {"raw": "P301A_4C", "std": "practica_recuperacion_salinos", "notes": "Agricultural practice."},
        {"raw": "P301A_5", "std": "practica_arar_tierra", "notes": "Agricultural practice."},
        {"raw": "P301A_6", "std": "practica_desterronar", "notes": "Agricultural practice."},
        {"raw": "P301A_7", "std": "practica_nivelar_terreno", "notes": "Agricultural practice."},
        {"raw": "P301A_8", "std": "practica_surcos_contorno", "notes": "Agricultural practice."},
        {"raw": "P301A_9", "std": "practica_agua_necesaria", "notes": "Agricultural practice."},
        {"raw": "P301A_10", "std": "practica_frecuencia_riego", "notes": "Agricultural practice."},
        {"raw": "P301A_11", "std": "practica_medir_agua", "notes": "Agricultural practice."},
        {"raw": "P301A_12", "std": "practica_mantenimiento_riego", "notes": "Agricultural practice."},
        {"raw": "P301A_12A", "std": "practica_analisis_agua", "notes": "Agricultural practice."},
        {"raw": "P301A_12B", "std": "practica_construccion_diques", "notes": "Agricultural practice."},
        {"raw": "P301A_12C", "std": "practica_waru_waru", "notes": "Agricultural practice."},
        {"raw": "P301A_13", "std": "practica_usar_abonos", "notes": "Agricultural practice."},
        {"raw": "P301A_14", "std": "practica_usar_fertilizantes", "notes": "Agricultural practice."},
        {"raw": "P301A_15", "std": "practica_usar_plaguicidas", "notes": "Agricultural practice."},
        {"raw": "P301A_16", "std": "practica_control_biologico", "notes": "Agricultural practice."},
        {"raw": "P301A_17", "std": "practica_manejo_integrado_plagas", "notes": "Agricultural practice."},
    ]


def main() -> None:
    if not DICT_PATH.exists():
        raise FileNotFoundError(f"Dictionary not found: {DICT_PATH}")

    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    dict_df = extract_dictionary(DICT_PATH)
    dict_csv = INTERMEDIATE_DIR / "ena2024_dictionary.csv"
    dict_df.to_csv(dict_csv, index=False)

    schema_map = build_schema_map()
    dict_lookup = dict(zip(dict_df["variable"], dict_df["description"]))

    table_rows = []
    for item in schema_map:
        raw = item["raw"]
        std = item["std"]
        description = dict_lookup.get(raw, "")
        unit = infer_unit(description) if description else ""
        notes = item.get("notes", "")
        table_rows.append(
            {
                "raw_variable": raw,
                "standard_name": std,
                "definition": description,
                "unit": unit,
                "notes": notes,
            }
        )

    dictionary_md = DOCS_DIR / "ENA2024_VARIABLE_DICTIONARY.md"
    with dictionary_md.open("w", encoding="utf-8") as handle:
        handle.write("# ENA 2024 Variable Dictionary (Mapped)\n\n")
        handle.write(f"- Generated: {dt.datetime.now().isoformat(timespec='seconds')}\n")
        handle.write(f"- Source: `{DICT_PATH}`\n\n")
        handle.write("| Variable original | Nombre estandarizado | Definicion | Unidad | Notas |\n")
        handle.write("|---|---|---|---|---|\n")
        for row in table_rows:
            handle.write(
                f"| {row['raw_variable']} | {row['standard_name']} | {row['definition']} | {row['unit']} | {row['notes']} |\n"
            )

    variable_map = {item["raw"]: item["std"] for item in schema_map}
    map_path = INTERMEDIATE_DIR / "variable_map.json"
    with map_path.open("w", encoding="utf-8") as handle:
        json.dump(variable_map, handle, indent=2, ensure_ascii=True)

    print(f"Wrote {dict_csv}")
    print(f"Wrote {dictionary_md}")
    print(f"Wrote {map_path}")


if __name__ == "__main__":
    sys.exit(main())
