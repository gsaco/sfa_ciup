#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
log_dir="$repo_root/logs"
mkdir -p "$log_dir"
timestamp="$(date +"%Y%m%d_%H%M%S")"
log_file="$log_dir/run_all_${timestamp}.log"

exec > >(tee "$log_file") 2>&1

echo "Running pipeline at $(date -Iseconds)"

python "$repo_root/src/ena/scan_repo.py"
python "$repo_root/src/ena/01_load_and_profile.py"
python "$repo_root/src/ena/02_build_schema_from_dictionary.py"
python "$repo_root/src/ena/03_apply_schema.py"
python "$repo_root/src/ena/04_compute_diversification.py"
pytest -q
python "$repo_root/src/ena/05_build_model_data.py"
Rscript "$repo_root/R/01_sfa_main.R"
Rscript "$repo_root/R/02_logit_practices.R"
python "$repo_root/src/report/build_report.py"

echo "Pipeline finished at $(date -Iseconds)"
