#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import logging
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
LOG_DIR = REPO_ROOT / "logs"


def setup_logger() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"geo_keys_profile_{timestamp}.log"
    logger = logging.getLogger("geo_keys_profile")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_path)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler())
    logger.info("Log path: %s", log_path)
    return logger


def pad_code(series: pd.Series, width: int) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    numeric = numeric.round().astype("Int64")
    return numeric.astype("string").str.zfill(width)


def main() -> None:
    logger = setup_logger()
    model_path = PROCESSED_DIR / "model_data_ena2024.parquet"
    if not model_path.exists():
        raise FileNotFoundError(f"Missing model data: {model_path}")

    df = pd.read_parquet(model_path)

    keys = ["ccdd", "ccpp", "ccdi"]
    for key in keys:
        if key not in df.columns:
            logger.info("Missing key column: %s", key)

    missing = {key: float(df[key].isna().mean()) for key in keys if key in df.columns}
    logger.info("Missing share (ccdd/ccpp/ccdi): %s", missing)

    if all(key in df.columns for key in keys):
        ccdd = pad_code(df["ccdd"], 2)
        ccpp = pad_code(df["ccpp"], 2)
        ccdi = pad_code(df["ccdi"], 2)
        ubigeo6 = (ccdd + ccpp + ccdi).where(
            ~(df["ccdd"].isna() | df["ccpp"].isna() | df["ccdi"].isna())
        )
        df = df.assign(ubigeo6=ubigeo6)
        unique_districts = df["ubigeo6"].nunique(dropna=True)
        logger.info("Unique ubigeo6 (non-missing): %s", unique_districts)
        examples = df["ubigeo6"].dropna().unique()[:5].tolist()
        logger.info("Example ubigeo6: %s", examples)
    else:
        logger.info("Cannot form ubigeo6: missing ccdd/ccpp/ccdi.")


if __name__ == "__main__":
    main()
