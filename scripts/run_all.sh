#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
log_dir="$repo_root/logs"
mkdir -p "$log_dir"
timestamp="$(date +"%Y%m%d_%H%M%S")"
log_file="$log_dir/run_all_${timestamp}.log"

python_bin="$repo_root/venv/bin/python"
if [ -x "$python_bin" ]; then
  PYTHON="$python_bin"
else
  PYTHON="python"
fi

exec > >(tee "$log_file") 2>&1

echo "Running pipeline at $(date -Iseconds)"

${PYTHON} "$repo_root/src/ena/scan_repo.py"
${PYTHON} "$repo_root/src/ena/01_load_and_profile.py"
${PYTHON} "$repo_root/src/ena/02_build_schema_from_dictionary.py"
${PYTHON} "$repo_root/src/ena/03_apply_schema.py"
${PYTHON} "$repo_root/src/ena/04_compute_diversification.py"
${PYTHON} "$repo_root/src/ena/05_build_model_data.py"
${PYTHON} "$repo_root/src/ena/06_build_model_data_plus_controls.py"
${PYTHON} "$repo_root/src/external/ubigeo/download_ubigeo_capitals.py"
${PYTHON} "$repo_root/src/external/ubigeo/parse_ubigeo_capitals.py"
${PYTHON} "$repo_root/src/external/chirps/download_chirps_monthly.py"
${PYTHON} "$repo_root/src/external/chirps/extract_chirps_points.py"
${PYTHON} "$repo_root/src/features/merge_geo_features.py"
${PYTHON} "$repo_root/src/external/temperature/find_source_and_document.py"
${PYTHON} "$repo_root/src/external/temperature/download_temperature_2023_2024.py"
${PYTHON} "$repo_root/src/external/temperature/extract_temperature_points.py"
${PYTHON} "$repo_root/src/features/merge_temperature_features.py"
${PYTHON} "$repo_root/src/external/topography/find_source_and_document.py"
${PYTHON} "$repo_root/src/external/topography/download_dem.py"
${PYTHON} "$repo_root/src/external/topography/extract_topography_points.py"
${PYTHON} "$repo_root/src/features/merge_geo2_features.py"
${PYTHON} "$repo_root/src/qa/sample_loss_analysis.py"
${PYTHON} -m pytest -q
Rscript "$repo_root/R/01_sfa_main.R"
Rscript "$repo_root/R/02_logit_practices.R"
${PYTHON} "$repo_root/src/report/build_report.py"

echo "Pipeline finished at $(date -Iseconds)"
