from __future__ import annotations

from typing import Iterable

import pandas as pd


def sum_components(df: pd.DataFrame, components: Iterable[str]) -> pd.Series:
    components = list(components)
    if not components:
        return pd.Series([pd.NA] * len(df), index=df.index, dtype="float")
    return df[components].sum(axis=1, min_count=1)


def component_missingness(df: pd.DataFrame, components: Iterable[str]) -> dict[str, float | int]:
    components = list(components)
    if not components:
        return {
            "n_rows": len(df),
            "n_all_missing": 0,
            "n_partial_missing": 0,
            "all_missing_share": float("nan"),
            "partial_missing_share": float("nan"),
            "any_missing_share": float("nan"),
        }

    subset = df[components]
    all_missing = subset.isna().all(axis=1)
    any_missing = subset.isna().any(axis=1)
    partial_missing = any_missing & ~all_missing
    return {
        "n_rows": int(len(subset)),
        "n_all_missing": int(all_missing.sum()),
        "n_partial_missing": int(partial_missing.sum()),
        "all_missing_share": float(all_missing.mean()) if len(subset) else float("nan"),
        "partial_missing_share": float(partial_missing.mean()) if len(subset) else float("nan"),
        "any_missing_share": float(any_missing.mean()) if len(subset) else float("nan"),
    }
