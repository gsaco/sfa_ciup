# Missingness Policy

This project treats missing values as unknowns, not zeros, unless a separate indicator explicitly implies zero.

## Principles
- **Missing != 0**: NA stays NA unless a clear "no" indicator implies the value is zero.
- **Aggregates**: Sums of components use `min_count=1`, so all-missing components yield NA and partial-missing rows sum the observed components.
- **Yes/No indicators**: Standardized mapping is used (`1 -> 1`, `2/0 -> 0`, other codes -> NA) and explicit `*_missing` flags are created.

## Explicit zero imputation
When a dedicated indicator makes zero logically implied, we fill zeros only under that condition (e.g., if `usuario_agua == 0`, then `gasto_agua_riego` is set to 0).

## Diagnostics
- `outputs/tables/19_missingness_audit.csv` reports:
  - share of rows with all components missing
  - share with partial missingness
  - overall missing share for key constructed variables

## Enforced locations
- Crop-level `valor_total_cultivo` (value-based diversification) uses `min_count=1` to avoid NA→0 in value totals.
- `labor_total`, `input_costs`, and other component sums in `src/ena/05_build_model_data.py` follow the same rule.

## Tests
Unit tests verify that all-missing component rows produce NA instead of 0.
