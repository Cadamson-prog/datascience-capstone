# Import-Position Linter

`src/scripts/linting/import_lint.py` checks that every `import` in the
repo's `.py` and `.ipynb` files appears at the top of the file, before
any other code.

It is a rule-checker, not a formatter, so it is not in the
`lint.sh` / `lint.bat` wrappers. Run it directly when you want to
check, or rely on the `import-lint` GitHub Actions job that runs on
every PR to `main`. See [`workflows/linting.md`](workflows/linting.md)
for the CI setup and recovery steps.

## Contents

- [The rule](#the-rule)
- [What's allowed before or among the imports](#whats-allowed-before-or-among-the-imports)
- [Notebooks (`.ipynb`)](#notebooks-ipynb)
- [Running the script](#running-the-script)
- [The report file](#the-report-file)
- [Reading the output](#reading-the-output)

## The rule

Every `import` and `from ... import ...` must appear at the top of the
file, before any other code. A violation is any `import` that appears
after non-import code at module scope. The script reports the offending
line and the location of the first non-import statement that triggered
the rule.

## What's allowed before or among the imports

These do not count as "code" and may appear before, between, or among
the imports:

- A shebang on the first line (e.g. `#!/usr/bin/env python`).
- Comments and blank lines.
- A single module-level docstring as the very first statement.
- Other import statements.
- A `try:` block whose entire body is itself only imports. Covers the
  common compatibility shim:

  ```python
  try:
      import cPickle as pickle
  except ImportError:
      import pickle
  ```

- An `if:` block whose entire body is itself only imports. Covers
  `TYPE_CHECKING` guards and version-conditional imports:

  ```python
  if TYPE_CHECKING:
      from foo import Bar
  ```

Anything else at module scope (assignments, function or class
definitions, function calls, etc.) counts as the start of "code", and
any `import` that follows it is a violation.

## Notebooks (`.ipynb`)

Markdown cells are ignored. They can sit at the top of the notebook or
between code cells without affecting the check.

Code cells are checked in order, as if their bodies were concatenated.
Once any code cell contains non-import code, every later `import` (in
that cell or any later code cell) is a violation. The first code cell
may start with a docstring; later cells may not.

IPython magics (`%matplotlib inline`, `!pip install ...`, `?help`) are
treated as no-ops so the linter can still parse cells that use them.

## Running the script

From anywhere inside the repo:

```bash
python src/scripts/linting/import_lint.py
```

The script:

1. Resolves the repo root via `git rev-parse --show-toplevel`.
2. Lists every tracked + new (non-gitignored) `.py` and `.ipynb` file
   via `git ls-files`.
3. Walks each file's module / cell body and flags any import that
   appears after non-import code.
4. Writes a Markdown report to `.artifacts_ci/import_lint_report.md`.

Exit codes:

- `0` if no violations are found.
- `1` if at least one violation was found, or if any file failed to
  parse.

## The report file

Every run writes a fresh Markdown report to
`.artifacts_ci/import_lint_report.md`. The directory is gitignored, so
the report never lands in a commit. A clean run still writes the file
with a single "no violations" line, so the artifact always reflects
the last run.

The report is grouped by file. For each offending file it lists:

- The location of the first non-import statement in that file (the
  thing that triggered the rule).
- Every late import, with its cell index (for notebooks), line number,
  and the actual import statement text rendered via `ast.unparse`.

There is no auto-fix. Move each late import yourself: top of the
notebook, top of an existing import block, or delete it if unused.

## Reading the output

A stderr line for one violation looks like:

```
notebooks/03_model_exploration/foo.ipynb cell 4 line 2: import pandas as pd
```

The corresponding entry in the report file:

```
## notebooks/03_model_exploration/foo.ipynb

First non-import code at: notebooks/03_model_exploration/foo.ipynb cell 0 line 5

Offending imports (1):

- notebooks/03_model_exploration/foo.ipynb cell 4 line 2: `import pandas as pd`
```

Read it as: the offending import is in cell 4 (0-indexed, code cells
only), line 2 of that cell. The first non-import statement was in cell
0 line 5, which is what made the late import a violation. To fix,
move the import up into a top-of-notebook import cell.

For `.py` files the format is the same minus the cell index:

```
src/utils/example.py line 42: import os
```
