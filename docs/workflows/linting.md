# Linting Workflows

CI linting workflows for the project:

- `py_lint.py` formats every Python file with
  [ruff](https://docs.astral.sh/ruff/). The `py-lint` GitHub Actions
  job enforces it on every PR to `main`.
- `import_lint.py` checks that every `import` in every `.py` and
  `.ipynb` file lives at the top of the file. The `import-lint`
  GitHub Actions job runs it on every PR to `main`. The rule itself
  is documented in [`../linting.md`](../linting.md); this doc covers
  only the CI side.

---

## Contents

- [Overview](#overview)
- [Running `py_lint.py` locally](#running-py_lintpy-locally)
- [GitHub Actions: `py-lint` job](#github-actions-py-lint-job)
- [Recovering from a failed `py-lint` job](#recovering-from-a-failed-py-lint-job)
- [GitHub Actions: `import-lint` job](#github-actions-import-lint-job)
- [Recovering from a failed `import-lint` job](#recovering-from-a-failed-import-lint-job)

---

## Overview

| Piece | Path |
| --- | --- |
| Linting script | `src/scripts/linting/py_lint.py` |
| Wrapper (macOS / Linux / Git Bash) | `lint.sh` |
| Wrapper (Windows cmd / PowerShell) | `lint.bat` |
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

## Running `py_lint.py` locally

### Prerequisites

- You are inside a clone of this repository.
- Your active Python environment has `ruff==0.15.12` installed:

  ```bash
  pip install ruff==0.15.12
  ```

  Or, equivalently, install via the project's pinned requirements:

  ```bash
  pip install -r requirements.txt
  ```

### Run it

The repo root ships two thin wrapper scripts that forward to
`src/scripts/linting/py_lint.py`. Use whichever fits your shell — both
resolve the underlying script relative to their own location, so they
work the same regardless of your current working directory.

**macOS / Linux / Git Bash:**

```bash
./lint.sh
```

**Windows cmd / PowerShell:**

```cmd
.\lint.bat
```

Either wrapper is equivalent to running the script directly:

```bash
python src/scripts/linting/py_lint.py
```

In all three cases, the script:

1. Resolves the repo root via `git rev-parse --show-toplevel`.
2. Lists every tracked + new (non-gitignored) `.py` file.
3. Runs `ruff format` on the full list, formatting in place.

After it finishes, inspect the changes with `git diff` and, if you accept
them, stage and commit:

```bash
git diff
git add -u
git commit -m "Apply ruff formatting"
```

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

2. **Run the linter locally** from the repo root, using whichever wrapper
   fits your shell:

   ```bash
   # macOS / Linux / Git Bash
   ./lint.sh
   ```

   ```cmd
   :: Windows cmd / PowerShell
   .\lint.bat
   ```

   (Or invoke the underlying script directly:
   `python src/scripts/linting/py_lint.py`.)

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

## GitHub Actions: `import-lint` job

The `.github/workflows/import-lint.yml` workflow runs on every pull
request that targets `main` (open, push, reopen) and on manual
`workflow_dispatch`. It uses the same `concurrency` group pattern as
`py-lint`, so pushing a new commit cancels the in-flight run for that
PR.

On `ubuntu-latest` the job:

1. Checks out the branch with full history.
2. Sets up Python 3.11. The script is stdlib-only, so no `pip install`
   step is needed.
3. Runs `python src/scripts/linting/import_lint.py`. The script writes
   a Markdown report to `.artifacts_ci/import_lint_report.md` and
   exits 0 (clean) or 1 (violations).
4. If the script exited non-zero, uploads the report as an artifact
   named `import_lint_report` and fails the job.

The `.artifacts_ci/` directory only exists on the runner for the
duration of the job. Locally the same path is gitignored. The report
shows up in two places: your local working tree after running the
script, and the workflow run page as a downloadable artifact.

There is no auto-fix. Move each late import yourself: top of the file,
top of an existing import block, or delete it if unused.

## Recovering from a failed `import-lint` job

If the `import-lint` job fails on your branch:

1. **Open the failed workflow run** on GitHub and download the
   `import_lint_report` artifact. It lists every offending import by
   file (and notebook cell, where applicable), with line number and
   import text.

2. **Run the linter locally** from the repo root to regenerate the
   same report and see the offending imports on stderr:

   ```bash
   python src/scripts/linting/import_lint.py
   ```

3. **Fix each violation.** Move every late import up into the
   top-of-file (or top-of-notebook) import block. If an import is
   unused, delete it instead. See [`../linting.md`](../linting.md) for
   the rule and allowed exceptions (shebangs, module docstrings,
   `try:` / `if:` blocks whose body is only imports, markdown cells
   in notebooks).

4. **Re-run the script** locally and confirm exit code 0 before
   pushing.

5. **Commit and push** your fixes:

   ```bash
   git add -u
   git commit -m "Move late imports to top of file"
   git push
   ```

6. **Re-run the workflow.** The push usually re-triggers `import-lint`
   automatically. You can also re-run it manually from the Actions tab
   on GitHub (or via `gh run rerun <run-id>`).

If the job still fails:

- Make sure you ran the script from inside the repo. It uses `git` to
  find the root and the file list.
- Make sure your fixes are pushed. A clean local tree is not enough;
  CI tests what is on the branch.
- Make sure you didn't introduce a new late import while moving an
  old one. The report will flag any new offender too.
