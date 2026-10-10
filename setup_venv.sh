#!/usr/bin/env bash
#
# Create (if missing) the project virtual environment in .venv/ and install
# dependencies from requirements.txt. Safe to re-run to pick up new
# requirements.
#
# Usage:
#   ./setup_venv.sh                 # uses python3 on PATH
#   PYTHON=python3.12 ./setup_venv.sh
#   source .venv/bin/activate

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

VENV_DIR=".venv"
PYTHON="${PYTHON:-python3}"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "[-] $PYTHON not found on PATH." >&2
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  echo "[+] Creating $VENV_DIR with $("$PYTHON" -V)"
  "$PYTHON" -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -r requirements.txt

echo "[✓] Done. Activate with: source $VENV_DIR/bin/activate"
