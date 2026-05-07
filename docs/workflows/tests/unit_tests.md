# `unit-tests` — Workflow Reference

A focused reference for the GitHub Actions workflow that runs the project's
unit test suite on every pull request targeting `main`.

---

## Contents

- [Overview](#overview)
- [Running the tests locally](#running-the-tests-locally)
- [GitHub Actions: `unit-tests` job](#github-actions-unit-tests-job)
- [Recovering from a failed `unit-tests` job](#recovering-from-a-failed-unit-tests-job)

---

## Overview

| Piece | Path |
| --- | --- |
| Test files | [`tests/unit/`](../../../tests/unit/) |
| Test directory README | [`tests/README.md`](../../../tests/README.md) |
| GitHub Actions workflow | [`.github/workflows/unit-tests.yml`](../../../.github/workflows/unit-tests.yml) |

The workflow runs `pytest` against the [`tests/unit/`](../../../tests/unit/)
directory. `pytest` auto-discovers every file matching the `test_*.py`
pattern (e.g. `test_fileops.py`, `test_py_lint.py`) and executes the test
cases inside each one. A non-zero exit code from `pytest` (any failing
test, collection error, or import error) fails the job. Model-level tests
are tracked separately under [`tests/model/`](../../../tests/model/) and
are not yet wired into CI.

---

## Running the tests locally

### Prerequisites

You have followed [`docs/DEVELOPER_SETUP.md`](../../DEVELOPER_SETUP.md) —
specifically:

- Created and activated a virtual environment.
- Installed dependencies from `requirements.txt` (`pytest` is included).
- Installed the project in editable mode (`pip install -e .`) so that
  `src.*` imports resolve.

### Run all tests

From the repo root (with the venv activated):

```bash
pytest tests/unit/
```

### Run a single file

```bash
pytest tests/unit/test_fileops.py
```

See [`tests/README.md`](../../../tests/README.md) for additional examples.

---

## GitHub Actions: `unit-tests` job

The [`.github/workflows/unit-tests.yml`](../../../.github/workflows/unit-tests.yml)
workflow runs on every pull request that targets `main` (when opened,
when new commits are pushed, and when reopened) and on manual
`workflow_dispatch`. PRs whose base branch is something other than
`main` (e.g. stacked feature branches) do not trigger the job, and it
does **not** run on close/merge. A `concurrency` group keyed on
`${{ github.workflow }}-${{ github.ref }}` with `cancel-in-progress: true`
ensures that pushing a new commit to a PR cancels the in-flight run for
that same PR — only the most recent commit is checked, since the job
validates the full PR file set rather than per-commit changes.

The job does the following on `ubuntu-latest`:

1. Checks out the branch.
2. Sets up Python 3.11 (with `pip` caching).
3. Installs runtime dependencies from `requirements.txt`.
4. Installs the project in editable mode (`pip install -e . --no-deps`)
   so test imports such as `import src.utils.fileops` resolve. `--no-deps`
   skips re-resolving the heavy ML dependencies already installed in step 3.
5. Runs `pytest tests/unit/ -v`.

The verbose flag (`-v`) makes each test name visible in the GitHub Actions
log so you can identify a failing test without downloading any artifacts.

---

## Recovering from a failed `unit-tests` job

If the `unit-tests` job fails on your branch:

1. **Open the failed workflow run on GitHub** and expand the "Run pytest"
   step. The pytest output names the failing test(s), the assertion that
   failed, and a traceback.

2. **Reproduce locally.** From the repo root with the venv activated:

   ```bash
   pytest tests/unit/ -v
   ```

   To re-run only the failing test (faster iteration):

   ```bash
   pytest tests/unit/test_<file>.py::TestClass::test_name -v
   ```

3. **Decide whether the test or the code is wrong:**

   - **Code regression** — your change broke behavior the test guards.
     Fix the source, then re-run pytest until it passes.
   - **Outdated test** — your change intentionally updated behavior, and
     the test needs to track that change. Update the test (and ideally
     mention the behavior change in your PR description), then re-run.
   - **Flaky / environmental failure** — uncommon for this suite (tests
     use `tmp_path` and mock I/O), but if you suspect this, re-run the
     workflow from the Actions tab. If it still fails, it's not flaky.

4. **Commit, push, re-run.** Pushing usually re-triggers the workflow
   automatically. You can also re-run it manually from the Actions tab
   on GitHub (or via `gh run rerun <run-id>`).

If the job still fails after these steps, double-check that:

- You ran `pip install -e .` after pulling — without it, `src.*` imports
  raise `ModuleNotFoundError` and the test file fails to collect.
- Your local Python version matches the workflow (3.11). The project
  supports `>=3.9`, but a wildly different version may surface
  version-specific behavior.
- New test files are named `test_*.py` so pytest discovers them. Files
  with other names (e.g. `fileops_tests.py`) are silently skipped.
