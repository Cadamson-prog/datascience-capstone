# Linting Workflows (GitHub Actions)

Two workflows enforce linting on every pull request to `main`. Both also run on manual `workflow_dispatch`.

| Workflow | File | Jobs |
|---|---|---|
| `lint` | [`.github/workflows/lint.yml`](../../.github/workflows/lint.yml) | `py-lint`, `nb-lint` |
| `import-lint` | [`.github/workflows/import-lint.yml`](../../.github/workflows/import-lint.yml) | `import-lint` |

When a job fails it uploads an artifact you can download from the workflow run page.

## Fixing a failed `py-lint` or `nb-lint`

These check that every `.py` and `.ipynb` is ruff-format-clean. The job uploads `py_lint_diff` or `nb_lint_diff` showing the formatting changes ruff wants to apply.

To fix:

1. Run the formatter locally. See [docs/linting.md](../linting.md) for the exact commands.
2. Review the diff, commit, and push.
3. The job re-runs on push.

## Fixing a failed `import-lint`

This checks that every `import` is at the top of its file. There is no auto-fix. The job uploads `import_lint_report`, a Markdown report listing every offending file, cell (for notebooks), line, and import text.

To fix:

1. Download the report and open it.
2. Manually move each late `import` to the top of its file (or top-of-notebook import cell). See [docs/linting.md](../linting.md) for the rule details and what is allowed.
3. Run the import-lint script locally and confirm exit code 0:

   ```bash
   python src/scripts/linting/import_lint.py
   ```

4. Commit, push, and the job re-runs.
