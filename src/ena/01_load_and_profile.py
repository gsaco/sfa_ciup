#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import logging
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(REPO_ROOT / "src"))

from ena.io import normalize_columns, read_csv


RAW_DIR = REPO_ROOT / "data" / "raw" / "ENA_2024"
INTERMEDIATE_DIR = REPO_ROOT / "data" / "intermediate"
LOG_DIR = REPO_ROOT / "logs"

KEY_COLS = ["ANIO", "CCDD", "CCPP", "CCDI", "NSEGM", "ID_PROD", "UA"]
DESIGN_COLS = ["ESTRATO", "FACTOR_PRODUCTOR", "FACTOR_SUPERFICIE", "NSEGM"]
POTENTIAL_CROP_ID_COLS = [
    "P115_COD",
    "P204_COD",
    "P229C_COD",
    "P229G_COD",
    "P234_COD",
    "P419_COD",
    "P1202_COD",
    "P1207_COD",
]


def setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"load_and_profile_{timestamp}.log"
    logger = logging.getLogger("ena_load_profile")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_path)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler())
    logger.info("Log path: %s", log_path)
    return logger


def profile_file(path: Path, logger: logging.Logger) -> dict[str, object]:
    header = read_csv(path, nrows=0)
    header = normalize_columns(header)
    cols = header.columns.tolist()

    key_cols = [c for c in KEY_COLS if c in cols]
    crop_id_cols = [c for c in POTENTIAL_CROP_ID_COLS if c in cols]
    design_cols = [c for c in DESIGN_COLS if c in cols]
    usecols = sorted(set(key_cols + crop_id_cols))

    df = read_csv(path, usecols=usecols if usecols else None, low_memory=False)
    df = normalize_columns(df)

    nrows = len(df)
    ncols = len(cols)
    missing = {}
    for col in key_cols:
        missing[col] = float(df[col].isna().mean())

    dup_keys = None
    if key_cols:
        dup_keys = int(df.duplicated(subset=key_cols).sum())

    dup_keys_crop = None
    crop_id = crop_id_cols[0] if crop_id_cols else ""
    if key_cols and crop_id:
        dup_keys_crop = int(df.duplicated(subset=key_cols + [crop_id]).sum())

    logger.info(
        "Profile %s | rows=%s cols=%s keys=%s dup_keys=%s crop_id=%s dup_keys_crop=%s",
        path.name,
        nrows,
        ncols,
        key_cols,
        dup_keys,
        crop_id,
        dup_keys_crop,
    )

    return {
        "file": path.relative_to(REPO_ROOT).as_posix(),
        "rows": nrows,
        "cols": ncols,
        "key_cols": ",".join(key_cols),
        "design_cols": ",".join(design_cols),
        "missing_keys": ";".join(f"{k}:{missing[k]:.4f}" for k in key_cols),
        "dup_keys": dup_keys,
        "crop_id_col": crop_id,
        "dup_keys_crop": dup_keys_crop,
    }


def main() -> None:
    logger = setup_logging()
    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)

    csv_paths = sorted(RAW_DIR.rglob("*.csv"))
    if not csv_paths:
        raise FileNotFoundError(f"No CSV files found under {RAW_DIR}")

    profiles = []
    for path in csv_paths:
        profiles.append(profile_file(path, logger))

    profile_df = pd.DataFrame(profiles)
    profile_path = INTERMEDIATE_DIR / "module_profile.csv"
    profile_df.to_csv(profile_path, index=False)
    logger.info("Wrote module profile: %s", profile_path)

    caratula_path = RAW_DIR / "973-Modulo1893" / "CARATULA.csv"
    if not caratula_path.exists():
        raise FileNotFoundError(f"Expected CARATULA at {caratula_path}")

    caratula = read_csv(caratula_path, low_memory=False)
    caratula = normalize_columns(caratula)
    logger.info("CARATULA rows=%s cols=%s", len(caratula), caratula.shape[1])

    missing_keys = {
        col: float(caratula[col].isna().mean())
        for col in KEY_COLS
        if col in caratula.columns
    }
    dup_keys = None
    if all(col in caratula.columns for col in KEY_COLS):
        dup_keys = int(caratula.duplicated(subset=KEY_COLS).sum())
    logger.info("CARATULA missing keys: %s", missing_keys)
    logger.info("CARATULA duplicate keys (ANIO+CCDD+CCPP+CCDI+NSEGM+ID_PROD+UA): %s", dup_keys)

    output_path = INTERMEDIATE_DIR / "ena2024_raw.parquet"
    caratula.to_parquet(output_path, index=False)
    logger.info("Wrote %s", output_path)


if __name__ == "__main__":
    main()
