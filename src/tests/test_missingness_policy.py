import pandas as pd

from ena.missingness import component_missingness, sum_components


def test_sum_components_all_missing_is_na():
    df = pd.DataFrame({"a": [pd.NA, 1], "b": [pd.NA, pd.NA]})
    result = sum_components(df, ["a", "b"])
    assert pd.isna(result.iloc[0]), "All-missing components should yield NA"
    assert result.iloc[1] == 1


def test_sum_components_partial_missing_keeps_value():
    df = pd.DataFrame({"a": [2, pd.NA], "b": [pd.NA, 3]})
    result = sum_components(df, ["a", "b"])
    assert result.iloc[0] == 2
    assert result.iloc[1] == 3


def test_component_missingness_counts():
    df = pd.DataFrame({"a": [pd.NA, 1, pd.NA], "b": [pd.NA, pd.NA, 2]})
    stats = component_missingness(df, ["a", "b"])
    assert stats["n_rows"] == 3
    assert stats["n_all_missing"] == 1
    assert stats["n_partial_missing"] == 2
