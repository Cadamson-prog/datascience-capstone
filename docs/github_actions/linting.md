# Linting Workflow

This document describes the project's GitHub Actions linting workflow:
the `py_lint.py` script that formats every Python file in the repository
with [ruff](https://docs.astral.sh/ruff/), the corresponding GitHub
Actions job that enforces it on every pull request targeting `main`,
and the steps to follow when that job fails.

For local linting (Python **and** Jupyter notebooks), see
[`docs/linting.md`](../linting.md).

---

## Contents

- [Overview](#overview)
- [GitHub Actions: `py-lint` job](#github-actions-py-lint-job)
- [Recovering from a failed `py-lint` job](#recovering-from-a-failed-py-lint-job)

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
| GitHub Actions workflow | `.github/workflows/py-lint.yml` |

The script discovers every Python file the repository tracks (and any new,
non-gitignored Python files staged for commit) using `git ls-files`,
then runs `ruff format` against the full list. Files are formatted in place;
no commits are created automatically.

The CI job runs the same script and then captures the resulting `git diff`.
A non-empty diff means the committed code does not match `ruff format`'s
expected output and the job fails.

---

## GitHub Actions: `py-lint` job

The `.github/workflows/py-lint.yml` workflow runs on every pull request
that targets `main` (when opened, when new commits are pushed, and when
reopened) and on manual `workflow_dispatch`. PRs whose base branch is
something other than `main` (e.g. stacked feature branches) do not
trigger the job, and it does **not** run on close/merge. A `concurrency`
group keyed on `${{ github.workflow }}-${{ github.ref }}` with
`cancel-in-progress: true` ensures that pushing a new commit to a PR
cancels the in-flight run for that same PR — only the most recent
commit is checked, since the job validates the full PR file set rather
than per-commit changes.

The job does the following on `ubuntu-latest`:

1. Checks out the branch (with full git history).
2. Sets up Python 3.11.
3. Installs `ruff==0.15.12`.
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
   exactly what `ruff format` wants to change.

2. **Run the linter locally** from the repo root. See
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

   This formats every Python file in place and should reproduce the same
   diff you downloaded.

3. **Stage and commit** the formatting changes:

   ```bash
   git add -u
   git commit -m "Apply ruff formatting"
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
- Your local `ruff` version matches the version installed in the workflow.
  Both are pinned to `ruff==0.15.12` (in `requirements.txt` and the workflow's
  install step). If your local version drifts, it will likely produce a
  different diff than CI. Reinstall the pin with `pip install ruff==0.15.12`
  or `pip install -r requirements.txt`.
