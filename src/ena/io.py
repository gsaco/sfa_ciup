from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


DEFAULT_ENCODINGS = ("utf-8", "latin-1", "cp1252")


def read_csv(path: str | Path, **kwargs: Any) -> pd.DataFrame:
    last_err: Exception | None = None
    for enc in DEFAULT_ENCODINGS:
        try:
            return pd.read_csv(path, encoding=enc, **kwargs)
        except UnicodeDecodeError as err:
            last_err = err
    if last_err is not None:
        raise last_err
    return pd.read_csv(path, **kwargs)


def read_dta(path: str | Path, **kwargs: Any) -> pd.DataFrame:
    return pd.read_stata(path, **kwargs)


def read_sav(path: str | Path, **kwargs: Any) -> pd.DataFrame:
    return pd.read_spss(path, **kwargs)


def read_xlsx(path: str | Path, **kwargs: Any) -> pd.DataFrame:
    return pd.read_excel(path, **kwargs)


def read_any(path: str | Path, **kwargs: Any) -> pd.DataFrame:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return read_csv(path, **kwargs)
    if suffix == ".dta":
        return read_dta(path, **kwargs)
    if suffix == ".sav":
        return read_sav(path, **kwargs)
    if suffix in {".xls", ".xlsx"}:
        return read_xlsx(path, **kwargs)
    raise ValueError(f"Unsupported file type: {suffix}")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    return df
