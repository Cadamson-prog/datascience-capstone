# Linting Workflow

This document describes the project's GitHub Actions linting workflow:
the `py_lint.py` and `nb_lint.py` scripts that format every Python file
and Jupyter notebook in the repository with
[ruff](https://docs.astral.sh/ruff/) (notebooks via
[nbQA](https://nbqa.readthedocs.io/)), the corresponding GitHub Actions
jobs that enforce them on every pull request targeting `main`, and the
steps to follow when either job fails.

For local linting (Python **and** Jupyter notebooks), see
[`docs/linting.md`](../linting.md).

---

## Contents

- [Overview](#overview)
- [GitHub Actions: `py-lint` and `nb-lint` jobs](#github-actions-py-lint-and-nb-lint-jobs)
- [Recovering from a failed lint job](#recovering-from-a-failed-lint-job)

---

## Overview

| Piece | Path |
| --- | --- |
| Python linting script | `src/scripts/linting/py_lint.py` |
| Notebook linting script | `src/scripts/linting/nb_lint.py` |
| Wrapper (macOS / Linux / Git Bash) | `lint.sh` |
| Wrapper (Windows cmd / PowerShell) | `lint.bat` |
| Local-linting walkthrough | [`docs/linting.md`](../linting.md) |
| Unit tests | `tests/unit/test_py_lint.py` |
| GitHub Actions workflow | `.github/workflows/lint.yml` |

`py_lint.py` discovers every Python file the repository tracks (and any
new, non-gitignored `.py` files staged for commit) using `git ls-files`,
then runs `ruff format` against the full list. `nb_lint.py` does the
same for `.ipynb` files, running `nbqa ruff format` so ruff is applied
to each notebook's code cells. Both scripts format files in place; no
commits are created automatically.

The CI jobs run the same scripts and then capture the resulting `git diff`.
A non-empty diff means the committed code does not match `ruff format`'s
expected output and the job fails.

---

## GitHub Actions: `py-lint` and `nb-lint` jobs

The `.github/workflows/lint.yml` workflow runs on every pull request
that targets `main` (when opened, when new commits are pushed, and when
reopened) and on manual `workflow_dispatch`. PRs whose base branch is
something other than `main` (e.g. stacked feature branches) do not
trigger the workflow, and it does **not** run on close/merge. A
`concurrency` group keyed on `${{ github.workflow }}-${{ github.ref }}`
with `cancel-in-progress: true` ensures that pushing a new commit to a
PR cancels the in-flight run for that same PR - only the most recent
commit is checked, since each job validates the full PR file set rather
than per-commit changes.

The workflow defines two jobs that run **in parallel** on
`ubuntu-latest`:

### `py-lint` job

1. Checks out the branch (with full git history).
2. Sets up Python 3.11.
3. Installs `ruff==0.15.12`.
4. Runs `python src/scripts/linting/py_lint.py` (which formats files in place).
5. Captures any resulting changes with `git diff > py_lint.diff`.
6. If `py_lint.diff` is non-empty, uploads it as an artifact named
   `py_lint_diff` and fails the job.

### `nb-lint` job

1. Checks out the branch (with full git history).
2. Sets up Python 3.11.
3. Installs `ruff==0.15.12` and `nbqa`.
4. Runs `python src/scripts/linting/nb_lint.py` (which formats notebooks in place).
5. Captures any resulting changes with `git diff > nb_lint.diff`.
6. If `nb_lint.diff` is non-empty, uploads it as an artifact named
   `nb_lint_diff` and fails the job.

Neither job commits or pushes the formatting changes. The diffs are
captured and surfaced as artifacts so you can review and apply them
locally. The two jobs are independent: one can pass while the other
fails, and each must succeed for the workflow to be green.

---

## Recovering from a failed lint job

If the `py-lint` or `nb-lint` job fails on your branch:

1. **Open the failed workflow run** on GitHub and download the
   `py_lint_diff` and/or `nb_lint_diff` artifact attached to the failing
   job(s). Each diff shows exactly what `ruff format` wants to change.

2. **Run the linters locally** from the repo root. See
   [`docs/linting.md`](../linting.md) for the full walkthrough; the short
   version is:

   ```bash
   # macOS / Linux / Git Bash
   ./lint.sh
   ```

   ```cmd
   :: Windows cmd / PowerShell
   .\lint.bat
   ```

   These wrappers run both `py_lint.py` and `nb_lint.py` in sequence,
   formatting every Python file and notebook in place, and should
   reproduce the same diff(s) you downloaded. To target only one
   language, invoke the relevant script directly:

   ```bash
   python src/scripts/linting/py_lint.py   # Python only
   python src/scripts/linting/nb_lint.py   # Notebooks only
   ```

3. **Stage and commit** the formatting changes:

   ```bash
   git add -u
   git commit -m "Apply ruff formatting"
   ```

4. **Push** to your branch:

   ```bash
   git push
   ```

5. **Re-run the workflow.** The push usually triggers `lint`
   automatically. You can also re-run it manually from the Actions tab
   on GitHub (or via `gh run rerun <run-id>`).

If the job still fails after these steps, double-check that:

- You ran the script(s) from inside the repository (each uses `git` to
  find the root and the file list).
- You committed and pushed the formatting changes (a clean working tree
  locally is necessary but not sufficient - the changes need to be on
  the branch CI is testing).
- Your local `ruff` version matches the version installed in the
  workflow. Both are pinned to `ruff==0.15.12` (in `requirements.txt`
  and the workflow's install steps). If your local version drifts, it
  will likely produce a different diff than CI. Reinstall the pin with
  `pip install ruff==0.15.12` or `pip install -r requirements.txt`.
- For notebook failures specifically, confirm `nbqa` is installed in
  your local environment (`pip install -r requirements.txt`).
