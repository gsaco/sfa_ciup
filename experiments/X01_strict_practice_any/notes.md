# Experiment X01: Strict practice_any definition

## Goal
Test whether a narrower "sustainable practices" subset reduces outcome saturation and changes logit results.

## Change
- Modified `src/ena/05_build_model_data.py` to compute `practice_any` and `num_practices` using a strict subset of P301A items (soil analysis, organic matter, rotation, terraces, water management, biological/IPM).
- Excluded routine practices (plowing, leveling, fertilizers, pesticides).

## BEFORE snapshot
- Run: `Rscript R/02_logit_practices.R` (see `logs/before.log`).
- Key outputs captured in `key_outputs_before/`.
- Baseline stats: `practice_any` mean approx 0.953; `num_practices` mean approx 7.06.

## AFTER run
- Rebuilt model data + merges + logit (see `logs/after.log`).
- Key outputs captured in `key_outputs_after/`.
- New stats: `practice_any` mean approx 0.867; `num_practices` mean approx 3.13.
- Logit main changes (04_logit_main.csv):
  - `diversificacion_area` OR dropped from ~15.46 to ~5.72.
  - `region_natural2` effect collapsed (OR ~1.0, non-significant).
  - `region_natural3` remained strongly negative.
- `usuario_agua=1` still implies `practice_any=1` ~99.6% (near-determinism persists).

## Decision (KEEP vs REVERT)
- **Decision:** REVERT.
- **Rationale:** This is a definitional choice, not a confirmed coding error. Results are sensitive but still show saturation; changing the outcome should be a substantive decision by the PI.

## Revert
- Restored original definition; rebuilt data and logit outputs (see `logs/revert.log`).

