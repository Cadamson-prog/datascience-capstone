# Unit Tests Workflow (GitHub Actions)

Runs the project's unit test suite on every pull request to `main`. Also runs on manual `workflow_dispatch`.

| Workflow | File | Job |
|---|---|---|
| `unit-tests` | [`.github/workflows/unit-tests.yml`](../../.github/workflows/unit-tests.yml) | `unit-tests` |

The job installs `requirements.txt`, installs the project in editable mode (`pip install -e . --no-deps`), and runs `pytest tests/unit/ -v`. Any failing test, collection error, or import error fails the job. Model-level tests under [`tests/model/`](../../tests/model/) are tracked separately and not yet wired into CI.

When the job fails, the failing test name and traceback are visible directly in the workflow log (the `-v` flag prints each test name). No artifact is uploaded.

## Fixing a failed `unit-tests`

1. Open the failed workflow run on GitHub and expand the "Run pytest" step. The log names the failing test and shows the assertion plus traceback.
2. Reproduce locally and iterate. See [docs/testing.md](../testing.md) for the commands.
3. Decide whether the test or the code is wrong:
   - **Code regression** ... your change broke behavior the test guards. Fix the source.
   - **Outdated test** ... your change intentionally updated behavior. Update the test (and mention the change in the PR description).
4. Commit, push, and the job re-runs.

If the job still fails after a clean local run, double-check that:

- You ran `pip install -e .` after pulling. Without it, `src.*` imports raise `ModuleNotFoundError` and test files fail to collect.
- New test files are named `test_*.py` so pytest discovers them. Files named otherwise (e.g. `fileops_tests.py`) are silently skipped.
