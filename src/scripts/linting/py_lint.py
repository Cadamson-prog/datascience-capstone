"""
Author: Brendan OConnell
Year:   2026

Purpose:
    Run the `ruff` formatter against every Python file tracked by the
    repository (and any new, non-gitignored Python files staged for commit).
    The script formats files in place and exits 0 if `ruff` itself succeeds.

    The companion GitHub Actions workflow (`.github/workflows/py-lint.yml`)
    invokes this script, captures any resulting `git diff`, uploads it as an
    artifact, and fails the job if the diff is non-empty.

Local usage:
    From the repository root, run:

        python src/scripts/linting/py_lint.py

    The script can be invoked from any working directory inside the repo;
    it resolves the repo root with `git rev-parse --show-toplevel`.

    Prerequisites:
        - You are inside a git repository.
        - `ruff==0.15.12` is installed in the active Python environment.
          Install with `pip install ruff==0.15.12`
          (or `pip install -r requirements.txt`) if needed.

How to recover from a failed GitHub Actions `py-lint` job:
    1. Download the `py_lint_diff` artifact from the workflow run to inspect
       the changes ruff wants to apply.
    2. Locally run `python src/scripts/linting/py_lint.py`.
    3. Stage the changes (`git add -u`), commit, and push.
    4. Re-run the workflow.

    See `docs/github_actions/linting.md` for the full walkthrough.
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
