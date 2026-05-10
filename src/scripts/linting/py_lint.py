"""
Author: Brendan OConnell
Year:   2026

Purpose:
    Run `ruff format` against every .PY script in the repository.
    Writes any formatting changes back to the Python files in place.
    Exits 0 if `ruff` succeeds.

Local usage:
    The script can be invoked from any working directory inside the repo.
    It resolves the repo root with `git rev-parse --show-toplevel`.

    To use, run:
        python src/scripts/linting/py_lint.py

Prerequisites:
    - `ruff` (check `requirements.txt` for pinned version).

See `docs/linting.md` for additional support.
"""

import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    """
    Return the absolute path to the repository root by asking git.

    Raises:
        RuntimeError: if the current working directory is not inside a git
            repository (or git is not installed).
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise RuntimeError(
            "Could not determine repository root. py_lint.py must be run "
            "inside a git repository with `git` available on PATH."
        ) from e
    return Path(result.stdout.strip())


def find_python_files(root: Path) -> list[Path]:
    """
    Return absolute paths to every .py file in the repo that git knows about
    (tracked files + new, non-gitignored files).

    Using `git ls-files` keeps the discovery aligned with `.gitignore`, so
    virtualenvs, build artifacts, and anything else excluded from the repo
    are skipped automatically.
    """
    tracked = subprocess.run(
        ["git", "ls-files", "*.py"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "*.py"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    rels = (tracked.stdout + untracked.stdout).splitlines()
    files = sorted({(root / rel).resolve() for rel in rels if rel})
    return files


def run_ruff(files: list[Path]) -> int:
    """
    Invoke `ruff format` on the given files. Returns ruff's exit code.
    Returns 0 immediately when there are no files to format.
    """
    if not files:
        print("No Python files to format.")
        return 0
    print(f"Running ruff format on {len(files)} file(s)...")
    cmd = [sys.executable, "-m", "ruff", "format", *[str(f) for f in files]]
    result = subprocess.run(cmd)
    return result.returncode


def main() -> int:
    root = repo_root()
    files = find_python_files(root)
    return run_ruff(files)


if __name__ == "__main__":
    sys.exit(main())
