#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(REPO_ROOT / "src"))

from external.ubigeo.download_ubigeo_fallback import main as download_fallback


RAW_DIR = REPO_ROOT / "data" / "external" / "raw" / "ubigeo"
PROCESSED_DIR = REPO_ROOT / "data" / "external" / "processed"

PLAN_A_PATH = RAW_DIR / "DD_TB_UBIGEOS.xlsx"
FALLBACK_PATH = RAW_DIR / "ubigeo_distrito.csv"


def parse_plan_a(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    df = pd.read_excel(path)
    cols = {c.lower() for c in df.columns}
    expected = {"latitud", "longitud", "superficie"}
    if not expected.intersection(cols):
        return None
    return df


def parse_fallback(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["ubigeo6"] = (
        pd.to_numeric(df["inei"], errors="coerce")
        .round()
        .astype("Int64")
        .astype("string")
        .str.zfill(6)
    )
    df = df[df["ubigeo6"].notna()].copy()
    df["ccdd"] = df["ubigeo6"].str.slice(0, 2)
    df["ccpp"] = df["ubigeo6"].str.slice(2, 4)
    df["ccdi"] = df["ubigeo6"].str.slice(4, 6)

    out = pd.DataFrame(
        {
            "ubigeo6": df["ubigeo6"],
            "ccdd": df["ccdd"],
            "ccpp": df["ccpp"],
            "ccdi": df["ccdi"],
            "departamento": df.get("departamento"),
            "provincia": df.get("provincia"),
            "distrito": df.get("distrito"),
            "capital_lat": pd.to_numeric(df.get("latitude"), errors="coerce"),
            "capital_lon": pd.to_numeric(df.get("longitude"), errors="coerce"),
            "surface_km2": pd.to_numeric(df.get("superficie"), errors="coerce"),
        }
    )
    return out


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df = parse_plan_a(PLAN_A_PATH)
    plan_used = "A"
    if df is None:
        download_fallback()
        df = parse_fallback(FALLBACK_PATH)
        plan_used = "B"

    output_path = PROCESSED_DIR / "ubigeo_district_capitals.parquet"
    df.to_parquet(output_path, index=False)

    plan_path = PROCESSED_DIR / "ubigeo_plan_used.json"
    plan_path.write_text(json.dumps({"plan_used": plan_used}, indent=2), encoding="utf-8")

    print(f"Wrote {output_path}")
    print(f"Plan used: {plan_used}")


if __name__ == "__main__":
    main()
