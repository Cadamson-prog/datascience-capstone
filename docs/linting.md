# Linting Locally

Run lint checks from the project root before committing. The same checks run in CI. 
See [docs/github_actions/linting.md](github_actions/linting.md) for the GitHub Actions side.

## Autoformat (py_lint + nb_lint)

Formats .PY and .IPYNB files in place using ruff (notebooks via nbqa). 
From the root directory, run the appropriate command for your shell:

**macOS / Linux:**

```bash
./lint.sh
```

**Windows:**

```powershell
lint.bat
```

Both wrappers run `py_lint.py` then `nb_lint.py`. After the script executes, any changes made will show up in source control (`git status` to view). Commit the format changes and push to the remote repository.

Running the lint script prior to pushing ensures that the GitHub CI `py-lint` and `nb-lint` jobs don't fail when they run for an open PR (they *will* fail if the pushed code does not match what the CI formatter expects).

## Import-position check (import_lint)

Checks that every `import` statement in every .PY and .IPYNB file lives at the top of the file, before any other code. Unlike the previous lint script, there is no auto-fix. Any offending import statements must be manually fixed, committed, and pushed.

Run from the project root:

```bash
python src/scripts/linting/import_lint.py
```

The script:

- Exits 0 if clean, 1 otherwise.
- Prints each offending import to stderr (file, line, import text, plus cell index for notebooks).
- Writes a Markdown report (grouped by file name) to `.artifacts_ci/import_lint_report.md` (gitignored).

To fix, open each file the report flags and move the offending `import` to the top before any other code. Re-run the script and confirm exit code 0 before pushing.

The following are allowed before or among the imports:

- a shebang on the first line: `#!`
- comments and blank lines
- a single module-level docstring
- `try:` or `if:` blocks whose body is only imports
- markdown cells in notebooks

