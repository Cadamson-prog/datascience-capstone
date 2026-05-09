#!/usr/bin/env bash
# Bootstrap the Python environment for this repo. Safe to re-run.
# Mirrors steps 1-3 of docs/DEVELOPER_SETUP.md (venv create, install
# requirements.txt, editable install of the project package).
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR=".venv"
PROMPT="datascience-capstone"

if [ -d "$VENV_DIR" ]; then
    echo "[devsetup] $VENV_DIR/ already exists, skipping venv creation."
else
    echo "[devsetup] Creating virtual environment in $VENV_DIR/ ..."
    python3 -m venv "$VENV_DIR" --prompt "$PROMPT"
fi

PIP="$VENV_DIR/bin/pip"
PYTHON="$VENV_DIR/bin/python"

echo "[devsetup] Upgrading pip ..."
"$PYTHON" -m pip install --upgrade pip

echo "[devsetup] Installing requirements.txt ..."
"$PIP" install -r requirements.txt

echo "[devsetup] Installing project as editable package ..."
"$PIP" install -e .

echo
echo "[devsetup] Done. Activate the venv in your shell with:"
echo "    source $VENV_DIR/bin/activate"
