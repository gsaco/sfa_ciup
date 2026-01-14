# Experiment X02: Standardize SFA Z variables

## Goal
Test whether standardizing diversification variables in the inefficiency (Z) equation reduces boundary `gamma` warnings and stabilizes SFA estimation.

## Change
- In `R/01_sfa_main.R`, standardized diversification variables (`diversificacion_area`, `shannon_area`, `num_crops_area`) and their size interactions before entering Z.
- Updated `z_names_main`, alt robustness Z terms, and comparison tables accordingly.

## BEFORE snapshot
- Run: `Rscript R/01_sfa_main.R` (see `logs/before.log`).
- Key outputs captured in `key_outputs_before/`.
- Warnings: repeated `gamma` near boundary; occasional singular covariance.

## AFTER run
- Run: `Rscript R/01_sfa_main.R` (see `logs/after.log`).
- Key outputs captured in `key_outputs_after/`.
- Result: **Warnings persisted** (gamma near 1; singular covariance still present).
- Coefficients rescaled as expected, but no convergence improvement.

## Decision (KEEP vs REVERT)
- **Decision:** REVERT.
- **Rationale:** Standardization did not resolve convergence warnings and complicates interpretability without clear benefit.

## Revert
- Restored original Z variable scaling; re-ran SFA (see `logs/revert.log`).

