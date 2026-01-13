from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


def _ensure_list(cols: Iterable[str]) -> list[str]:
    return list(cols)


def compute_diversification(
    df: pd.DataFrame,
    id_cols: Iterable[str],
    value_col: str,
    crop_col: str,
) -> pd.DataFrame:
    id_cols = _ensure_list(id_cols)
    data = df[id_cols + [value_col, crop_col]].copy()
    data[value_col] = pd.to_numeric(data[value_col], errors="coerce")

    totals = data.groupby(id_cols)[value_col].transform("sum")
    data = data[totals > 0].copy()
    if data.empty:
        return pd.DataFrame(columns=id_cols + ["hhi", "diversificacion", "shannon", "num_crops", "total_value"])

    data["share"] = data[value_col] / totals[totals > 0]
    data = data[data["share"] > 0]

    grouped = data.groupby(id_cols, dropna=False)
    hhi = grouped["share"].apply(lambda x: float((x**2).sum()))
    shannon = grouped["share"].apply(lambda x: float(-(x * np.log(x)).sum()))
    num_crops = grouped[crop_col].nunique()
    total_value = grouped[value_col].sum()

    out = pd.DataFrame(
        {
            "hhi": hhi,
            "diversificacion": 1 - hhi,
            "shannon": shannon,
            "num_crops": num_crops,
            "total_value": total_value,
        }
    ).reset_index()
    return out
