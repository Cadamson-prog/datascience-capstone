#!/usr/bin/env bash
# Convenience wrapper that runs both linting scripts:
#   - src/scripts/linting/py_lint.py  (Python files)
#   - src/scripts/linting/nb_lint.py  (Jupyter notebooks)
# Locates the scripts relative to this file, so it runs the same way from any
# working directory. Any arguments are forwarded to both scripts.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python "$SCRIPT_DIR/src/scripts/linting/py_lint.py" "$@"
python "$SCRIPT_DIR/src/scripts/linting/nb_lint.py" "$@"
