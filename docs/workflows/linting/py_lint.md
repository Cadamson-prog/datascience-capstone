# `py_lint.py` — Script Reference

A focused reference for the linting script invoked by the `py-lint` GitHub
Actions job. For the full workflow walkthrough (overview, recovery steps,
troubleshooting), see [`docs/workflows/linting.md`](../linting.md).

---

## What it does

`src/scripts/linting/py_lint.py` runs [black](https://black.readthedocs.io/)
against every Python file in the repository, formatting them in place.

File discovery uses `git ls-files`, so the list automatically respects
`.gitignore` and includes both:

- tracked `.py` files
- new, non-gitignored `.py` files (staged or unstaged)

---

## Run it locally

```bash
# from any directory inside the repo
python src/scripts/linting/py_lint.py
```

Prerequisites:

- Inside a git repository (script uses `git rev-parse --show-toplevel`).
- `black` installed in the active Python environment
  (`pip install black`).

After running, inspect with `git diff` and commit if you accept the
changes.

---

## When the `py-lint` GitHub Actions job fails

The job fails because `black` produced changes against the committed code.
To recover:

1. Download the `py_lint_diff` artifact from the failed workflow run.
   It contains the exact diff that caused the failure.
2. Locally run:

   ```bash
   python src/scripts/linting/py_lint.py
   ```

3. Stage and commit the formatting changes:

   ```bash
   git add -u
   git commit -m "Apply black formatting"
   ```

4. Push to your branch and re-run the workflow.

For the longer-form walkthrough and troubleshooting tips, see
[`docs/workflows/linting.md`](../linting.md).
