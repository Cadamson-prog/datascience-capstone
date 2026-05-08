# Import-Position Linter

This document describes `src/scripts/linting/import_lint.py`, an opt-in
linter that verifies every `import` statement in the repository's Python
sources and Jupyter notebooks appears at the top of the file, before any
non-import code.

Unlike the Ruff-based formatters described in
[`workflows/linting.md`](workflows/linting.md), this script is not wired
into `lint.sh` / `lint.bat`, and it does not run in CI. Run it manually
when you want to verify import-position hygiene across the repo.

## Contents

- [The rule](#the-rule)
- [What's allowed before or among the imports](#whats-allowed-before-or-among-the-imports)
- [Notebooks (`.ipynb`)](#notebooks-ipynb)
- [Running the script](#running-the-script)
- [The report file](#the-report-file)
- [Reading the output](#reading-the-output)
- [Why this is not in `lint.sh` / `lint.bat`](#why-this-is-not-in-lintsh--lintbat)

## The rule

All `import` and `from ... import ...` statements must appear at the top
of the file, before any other code.

A violation is any `import` that appears after non-import code at module
scope. The script reports the offending line and the location of the
first non-import statement that triggered the violation.

## What's allowed before or among the imports

The following are not considered "code" for purposes of this rule and
may appear before, between, or among the imports:

- A shebang on the first line (e.g. `#!/usr/bin/env python`).
- Comments and blank lines.
- A single module-level docstring as the very first statement.
- Other import statements.
- A `try:` block whose entire body is itself only imports. This covers
  the common compatibility shim:

  ```python
  try:
      import cPickle as pickle
  except ImportError:
      import pickle
  ```

- An `if:` block whose entire body is itself only imports. This covers
  `TYPE_CHECKING` guards and version-conditional imports:

  ```python
  if TYPE_CHECKING:
      from foo import Bar
  ```

Anything else at module scope (assignments, function or class
definitions, function calls, etc.) counts as the start of "code", and
any `import` that follows it is a violation.

## Notebooks (`.ipynb`)

Markdown cells are ignored entirely. They may appear at the top of the
notebook (the intended pattern for titles and section descriptions) or
interleaved between code cells without affecting the check.

Code cells are checked in order, as if their bodies were concatenated.
Once any code cell contains non-import code, every subsequent `import`
(in that cell or any later code cell) is a violation. This catches the
common notebook anti-pattern of importing a new library halfway through
the notebook.

The first code cell is allowed to begin with a docstring; later code
cells are not.

IPython magics (`%matplotlib inline`, `!pip install ...`, `?help`) are
silently treated as no-ops so the linter can parse cells that use them.

## Running the script

From anywhere inside the repo:

```bash
python src/scripts/linting/import_lint.py
```

The script:

1. Resolves the repo root via `git rev-parse --show-toplevel`.
2. Lists every tracked + new (non-gitignored) `.py` and `.ipynb` file
   via `git ls-files`.
3. Walks each file's module / cell body and reports any import that
   appears after non-import code.
4. Writes a Markdown report to `.artifacts_ci/import_lint_report.md`
   (see below).

Exit codes:

- `0` if no violations are found.
- `1` if at least one violation was found, or if any file failed to
  parse.

## The report file

On every run the script writes a fresh Markdown report to
`.artifacts_ci/import_lint_report.md` at the repo root. The
`.artifacts_ci/` directory is gitignored so the report never gets
committed.

The report is grouped by file. For each offending file it lists:

- The location of the first non-import statement in that file (the
  thing that triggered the rule).
- Every late import, with its cell index (for notebooks), line number,
  and the actual import statement text rendered with `ast.unparse`.

A clean run still writes the file, with a single "no violations" line
so the artifact always reflects the latest run.

The script does not auto-fix anything. Each late import has to be moved
by hand because where it belongs is a judgment call (top of the
notebook, top of an existing import block, or removed entirely if
unused).

## Reading the output

A stderr line for one violation looks like:

```
notebooks/03_model_exploration/foo.ipynb cell 4 line 2: import pandas as pd
```

The corresponding entry in the report file is:

```
## notebooks/03_model_exploration/foo.ipynb

First non-import code at: notebooks/03_model_exploration/foo.ipynb cell 0 line 5

Offending imports (1):

- notebooks/03_model_exploration/foo.ipynb cell 4 line 2: `import pandas as pd`
```

Read it as: the offending import lives in cell 4 (0-indexed, code cells
only), on line 2 within that cell. The first non-import statement in
this notebook was in cell 0 line 5, which is what made the late import
a violation. To fix it, move the late import up into a top-of-notebook
import cell, or up to immediately above that cell-0 line if all the
imports belong together.

For `.py` files the format is similar but without the cell index:

```
src/utils/example.py line 42: import os
```

## Why this is not in `lint.sh` / `lint.bat`

The two wrappers in the repo root (`lint.sh`, `lint.bat`) intentionally
forward only to the formatting linters (`py_lint.py`, `nb_lint.py`),
which apply Ruff in place. Those scripts are safe to run unattended:
they fix what they can and leave a reviewable diff.

`import_lint.py` is a rule-checker, not a formatter. It surfaces issues
that a human has to fix by deciding where each late import belongs.
There is no automatic rewrite. Bundling it into the wrappers would
either silently swallow violations (if it ran with `|| true`) or break
the wrapper's "format and move on" contract for everyone running the
formatters.

If you want the rule enforced in CI later, add it as its own GitHub
Actions job (parallel to `py-lint` and `nb-lint`) rather than chaining
it into the formatter wrappers.
