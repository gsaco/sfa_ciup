import math

import pandas as pd

from features.diversification import compute_diversification


def test_diversification_two_crops():
    df = pd.DataFrame(
        {
            "id": [1, 1, 2],
            "crop": ["A", "B", "A"],
            "area": [1.0, 1.0, 2.0],
        }
    )
    result = compute_diversification(df, id_cols=["id"], value_col="area", crop_col="crop")
    row1 = result[result["id"] == 1].iloc[0]
    row2 = result[result["id"] == 2].iloc[0]

    assert math.isclose(row1["hhi"], 0.5, rel_tol=1e-6)
    assert math.isclose(row1["diversificacion"], 0.5, rel_tol=1e-6)
    assert math.isclose(row1["shannon"], math.log(2), rel_tol=1e-6)
    assert row1["num_crops"] == 2

    assert math.isclose(row2["hhi"], 1.0, rel_tol=1e-6)
    assert math.isclose(row2["diversificacion"], 0.0, rel_tol=1e-6)
    assert row2["num_crops"] == 1
