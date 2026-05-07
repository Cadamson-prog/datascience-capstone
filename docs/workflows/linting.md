# Linting Workflow

This document describes the project's Python linting workflow:
the `py_lint.py` script that formats every Python file in the repository
with [black](https://black.readthedocs.io/), the corresponding GitHub
Actions job that enforces it on every pull request and push to `main`,
and the steps to follow when that job fails.

---

## Contents

- [Overview](#overview)
- [Running `py_lint.py` locally](#running-py_lintpy-locally)
- [GitHub Actions: `py-lint` job](#github-actions-py-lint-job)
- [Recovering from a failed `py-lint` job](#recovering-from-a-failed-py-lint-job)

---

## Overview

| Piece | Path |
| --- | --- |
| Linting script | `src/scripts/linting/py_lint.py` |
| Script-specific doc | `docs/workflows/linting/py_lint.md` |
| Unit tests | `tests/test_py_lint.py` |
| GitHub Actions workflow | `.github/workflows/py-lint.yml` |

The script discovers every Python file the repository tracks (and any new,
non-gitignored Python files staged for commit) using `git ls-files`,
then runs `black` against the full list. Files are formatted in place;
no commits are created automatically.

The CI job runs the same script and then captures the resulting `git diff`.
A non-empty diff means the committed code does not match `black`'s expected
output and the job fails.

---

## Running `py_lint.py` locally

### Prerequisites

- You are inside a clone of this repository.
- Your active Python environment has `black` installed:

  ```bash
  pip install black
  ```

### Run it

From any directory inside the repo:

```bash
python src/scripts/linting/py_lint.py
```

The script:

1. Resolves the repo root via `git rev-parse --show-toplevel`.
2. Lists every tracked + new (non-gitignored) `.py` file.
3. Runs `black` on the full list, formatting in place.

After it finishes, inspect the changes with `git diff` and, if you accept
them, stage and commit:

```bash
git diff
git add -u
git commit -m "Apply black formatting"
```

---

## GitHub Actions: `py-lint` job

The `.github/workflows/py-lint.yml` workflow runs on every pull request,
every push to `main`, and on manual `workflow_dispatch`. The job does the
following on `ubuntu-latest`:

1. Checks out the branch (with full git history).
2. Sets up Python 3.11.
3. Installs `black`.
4. Runs `python src/scripts/linting/py_lint.py` (which formats files in place).
5. Captures any resulting changes with `git diff > py_lint.diff`.
6. If `py_lint.diff` is non-empty, uploads it as an artifact named
   `py_lint_diff` and fails the job.

The job **does not** commit or push the formatting changes. The diff is
captured and surfaced as an artifact so you can review and apply it locally.

---

## Recovering from a failed `py-lint` job

If the `py-lint` job fails on your branch:

1. **Open the failed workflow run** on GitHub and download the
   `py_lint_diff` artifact attached to the `py-lint` job. The diff shows
   exactly what `black` wants to change.

2. **Run `py_lint.py` locally** from the repo root:

   ```bash
   python src/scripts/linting/py_lint.py
   ```

   This formats every Python file in place and should reproduce the same
   diff you downloaded.

3. **Stage and commit** the formatting changes:

   ```bash
   git add -u
   git commit -m "Apply black formatting"
   ```

4. **Push** to your branch:

   ```bash
   git push
   ```

5. **Re-run the workflow.** The push usually triggers `py-lint` automatically.
   You can also re-run it manually from the Actions tab on GitHub
   (or via `gh run rerun <run-id>`).

If the job still fails after these steps, double-check that:

- You ran the script from inside the repository (it uses `git` to find the
  root and the file list).
- You committed and pushed the formatting changes (a clean working tree
  locally is necessary but not sufficient — the changes need to be on the
  branch CI is testing).
- Your local `black` version matches the version installed in the workflow.
  The workflow installs the latest release; if your local version is older
  it may produce a different diff. Update with `pip install --upgrade black`.
