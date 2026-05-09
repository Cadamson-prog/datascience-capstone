# Linting Locally

Two repo-root wrappers run both linters back-to-back: `py_lint.py` (Python
files via [ruff](https://docs.astral.sh/ruff/)) and `nb_lint.py` (Jupyter
notebooks via [nbQA](https://nbqa.readthedocs.io/) + ruff). Each formats
in place - review the diff before committing.

For the GitHub Actions side of these jobs, see
[`docs/github_actions/linting.md`](github_actions/linting.md).

---

## Prerequisites

- You are inside a clone of this repository.
- Your active Python environment has the linting dependencies installed:

  ```bash
  pip install -r requirements.txt
  ```

  (Pinned: `ruff==0.15.12`. `nbqa` is also required for notebook linting.)

---

## Run it

**macOS / Linux / Git Bash:**

```bash
./lint.sh
```

**Windows cmd / PowerShell:**

```cmd
.\lint.bat
```

Both wrappers run, in order:

1. `python src/scripts/linting/py_lint.py` - formats every tracked
   (and new, non-gitignored) `.py` file with `ruff format`.
2. `python src/scripts/linting/nb_lint.py` - formats every tracked
   (and new, non-gitignored) `.ipynb` file with `nbqa ruff format`.

You can also invoke either script on its own:

```bash
python src/scripts/linting/py_lint.py
python src/scripts/linting/nb_lint.py
```

---

## Review and commit

After the wrapper finishes, inspect any changes and commit them:

```bash
git diff
git add -u
git commit -m "Apply ruff formatting"
```

---

## Notebook lint configuration

Ruff's notebook-specific rules are configured in
[`pyproject.toml`](../pyproject.toml) under
`[tool.ruff.lint.per-file-ignores]` with a `*.ipynb` glob. The current
exemptions cover common notebook patterns (imports in non-first cells,
imports kept for later cells, long `pd.set_option(...)` lines). Update
that section if you need to add or remove rules for notebooks.
