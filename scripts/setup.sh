#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python_bin="${PYTHON_BIN:-python3}"
venv_dir="$repo_root/venv"

if [ ! -d "$venv_dir" ]; then
  "$python_bin" -m venv "$venv_dir"
fi

# shellcheck disable=SC1091
source "$venv_dir/bin/activate"

python -m pip install --upgrade pip
pip install -r "$repo_root/requirements.txt"

if ! command -v Rscript >/dev/null 2>&1; then
  echo "Rscript not found. Install R before running setup." >&2
  exit 1
fi

Rscript "$repo_root/R/install_packages.R"

echo "Setup complete. Activate with: source venv/bin/activate"
