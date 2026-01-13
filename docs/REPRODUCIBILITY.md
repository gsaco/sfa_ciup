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

Logs are written to `logs/run_all_YYYYMMDD_HHMMSS.log`.

## Inputs
- Raw ENA 2024 files live in `data/raw/ENA_2024/` and `data/ENA_2024.zip`.
- Variable dictionary: `DICCIONARIO DE DATOS ENA-2024.pdf`.

## Outputs
- Final report: `reports/reporte_final.md`
- Tables: `outputs/tables/*.csv` and `outputs/tables/*.md`
- Manifest: `outputs/manifest.json`

## Versions
- R 4.5.1 and packages: `frontier`, `survey`, `broom`
- Python: `numpy`, `pandas`, `pdfplumber`, `pyarrow`, `pytest`, `tabulate`

## Seeds
No stochastic procedures were used in the pipeline. If randomization is added later, set explicit seeds in each script.
