# Reproducibility

## Quick setup (venv + R packages)
```bash
./scripts/setup.sh
source venv/bin/activate
```

## One-command pipeline
```bash
./scripts/run_all.sh
```

The pipeline downloads external climate/topography sources and caches them under
`data/external/raw/`. Re-running will reuse cached files when present.

## CHIRPS baseline window
By default, the pipeline uses a reduced baseline window (2015–2020) for CHIRPS due to download constraints. You can override via:
```bash
CHIRPS_BASELINE_START=1991 CHIRPS_BASELINE_END=2020 CHIRPS_MAX_FILES=400 ./scripts/run_all.sh
```

Logs are written to `logs/run_all_YYYYMMDD_HHMMSS.log`.

## Inputs
- Raw ENA 2024 files live in `data/raw/ENA_2024/` and `data/ENA_2024.zip`.
- Variable dictionary: `DICCIONARIO DE DATOS ENA-2024.pdf`.

## Outputs
- Final report: `reports/reporte_final.md`
- Tables: `outputs/tables/*.csv` and `outputs/tables/*.md`
- Manifest: `outputs/manifest.json`
- Processed datasets: `data/processed/model_data_ena2024_plus_controls.*` and `data/processed/model_data_ena2024_plus_geo2.*`

## Versions
- R 4.5.1 and packages: `frontier`, `survey`, `broom`
- Python: `numpy`, `pandas`, `pdfplumber`, `pyarrow`, `pytest`, `tabulate`, `openpyxl`, `rasterio`

## Seeds
No stochastic procedures were used in the pipeline. If randomization is added later, set explicit seeds in each script.
