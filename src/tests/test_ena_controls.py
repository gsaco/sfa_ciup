from pathlib import Path

import pandas as pd
import pytest


def read_parquet_or_csv(path: Path) -> pd.DataFrame:
    try:
        return pd.read_parquet(path)
    except OSError as exc:
        csv_path = path.with_suffix(".csv")
        if not csv_path.exists():
            pytest.skip(f"Unable to read parquet {path} and missing {csv_path}: {exc}")
        return pd.read_csv(csv_path)


def test_ena_controls_dataset():
    path = Path("data/processed/model_data_ena2024_plus_controls.parquet")
    assert path.exists(), "Missing plus controls dataset"
    df = read_parquet_or_csv(path)

    expected_cols = [
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
    for col in expected_cols:
        assert col in df.columns, f"Missing column {col}"

    dummy_cols = [
        "riego_any",
        "riego_tecnificado_any",
        "usuario_agua",
        "uso_maquinaria",
        "usa_abono",
        "usa_fertilizantes",
        "semilla_semillero_any",
        "semilla_comercial_any",
        "semilla_certificada_any",
        "capacitacion_recibida",
        "asistencia_tecnica_recibida",
        "credito_obtenido",
        "asociacion_miembro",
    ]
    for col in dummy_cols:
        vals = set(df[col].dropna().unique())
        assert vals.issubset({0, 1}), f"Non-binary values in {col}: {vals}"

    share_cols = ["riego_share", "riego_tecnificado_share", "semilla_certificada_share"]
    for col in share_cols:
        assert df[col].dropna().between(0, 1).mean() > 0.95

    nonneg_cols = [
        "gasto_agua_riego",
        "num_maquinaria_equipo",
        "gasto_compra_equipos",
        "gasto_compra_maquinaria",
        "gasto_alquiler_mant_equipos",
        "gasto_semilla",
        "asociacion_num",
    ]
    for col in nonneg_cols:
        assert (df[col].dropna() >= 0).mean() > 0.95

    assert df["nivel_educacion"].between(1, 10).mean() > 0.9
