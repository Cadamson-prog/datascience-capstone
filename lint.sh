#!/usr/bin/env bash
# Convenience wrapper for src/scripts/linting/py_lint.py.
# Locates the script relative to this file, so it runs the same way from any
# working directory. Any arguments are forwarded to py_lint.py.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python "$SCRIPT_DIR/src/scripts/linting/py_lint.py" "$@"
