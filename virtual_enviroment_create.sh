#!/usr/bin/env bash

# Purpose: Create and activate a Python virtual environment, then install dependencies.
# Naming (follow these defaults unless you change them):
# - Virtual environment directory name: .venv
# - Activation path: .venv/bin/activate

# python3 -m venv-linkedin-bot && source venv-linkedin-bot/bin/activate

set -euo pipefail

# Always run from the repo root (directory containing this script)
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)
cd "$SCRIPT_DIR"

# Configuration (can be overridden via env)
VENV_DIR=${VENV_DIR:-venv-linkedin-bot}
PYTHON=${PYTHON:-python3}

echo
echo "[+] Using Python: $($PYTHON -V 2>/dev/null || echo 'python3 not found')"

# Ensure python3 exists
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "[-] Error: python3 is not installed or not on PATH."
  exit 1
fi

# Create venv if missing
if [ ! -d "$VENV_DIR" ]; then
  echo "[+] Creating virtual environment in $VENV_DIR"
  "$PYTHON" -m venv "$VENV_DIR"
else
  echo "[=] Virtual environment already exists at $VENV_DIR"
fi

# Activate venv
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"
echo "[+] Activated virtual environment: $VIRTUAL_ENV"

# Upgrade pip tooling (safe, within venv)
python -m pip install --upgrade pip setuptools wheel

# Install requirements if present
if [ -f requirements.txt ]; then
  echo "[+] Installing requirements from requirements.txt"
  python -m pip install -r requirements.txt
else
  echo "[=] No requirements.txt found; skipping dependency install"
fi

echo "[✓] Done."
echo
echo "NOTE: The venv was created but not activated in your current shell."
echo "To activate it, run:"
echo "    source $VENV_DIR/bin/activate"
echo "To deactivate later, run:"
echo "    deactivate"
