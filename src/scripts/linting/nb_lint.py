"""
Author: Brendan OConnell
Year:   2026

Purpose:
    Run `ruff format` against every Jupyter notebook tracked by the
    repository (and any new, non-gitignored `.ipynb` files staged for
    commit). The notebooks are linted via `nbqa`, which extracts each
    code cell, runs ruff against it, and writes any formatting changes
    back to the notebook in place.

    Ruff's lint configuration for notebooks lives in `pyproject.toml`
    under `[tool.ruff.lint.per-file-ignores]` with a `*.ipynb` glob.

Local usage:
    From the repository root, run:

        python src/scripts/linting/nb_lint.py

    The script can be invoked from any working directory inside the repo;
    it resolves the repo root with `git rev-parse --show-toplevel`.

    Prerequisites:
        - You are inside a git repository.
        - `ruff==0.15.12` and `nbqa` are installed in the active Python
          environment. Install with `pip install -r requirements.txt`
          if needed.

See `docs/linting.md` for the full local-linting walkthrough.
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
            "Could not determine repository root. nb_lint.py must be run "
            "inside a git repository with `git` available on PATH."
        ) from e
    return Path(result.stdout.strip())


def find_notebook_files(root: Path) -> list[Path]:
    """
    Return absolute paths to every .ipynb file in the repo that git knows
    about (tracked files + new, non-gitignored files).

    Using `git ls-files` keeps the discovery aligned with `.gitignore`, so
    checkpoints and anything else excluded from the repo are skipped
    automatically.
    """
    tracked = subprocess.run(
        ["git", "ls-files", "*.ipynb"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "*.ipynb"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    rels = (tracked.stdout + untracked.stdout).splitlines()
    files = sorted({(root / rel).resolve() for rel in rels if rel})
    return files


def run_nbqa_ruff(files: list[Path]) -> int:
    """
    Invoke `nbqa ruff format` on the given notebooks. Returns the exit code.
    Returns 0 immediately when there are no files to format.
    """
    if not files:
        print("No Jupyter notebooks to format.")
        return 0
    print(f"Running nbqa + ruff format on {len(files)} notebook(s)...")
    # `nbqa` parses its first positional argument as a single tool name, so
    # to run the `ruff format` *subcommand* we pass the whole string under
    # `--nbqa-shell` (which executes `command` directly instead of via
    # `python -m <command>`).
    cmd = [
        sys.executable,
        "-m",
        "nbqa",
        "--nbqa-shell",
        "ruff format",
        *[str(f) for f in files],
    ]
    result = subprocess.run(cmd)
    return result.returncode


def main() -> int:
    root = repo_root()
    files = find_notebook_files(root)
    return run_nbqa_ruff(files)


if __name__ == "__main__":
    sys.exit(main())
