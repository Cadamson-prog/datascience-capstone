# Testing Locally

The [`tests/`](../tests/) directory has two subdirectories:

- [`tests/unit/`](../tests/unit/) - unit tests for source code in [`src/`](../src/).
- [`tests/model/`](../tests/model/) - reserved for forthcoming model tests (logistic regression, XGBoost, neural network). Not yet implemented.

### Prerequisites

Follow [`DEVELOPER_SETUP.md`](DEVELOPER_SETUP.md) to get your Python environment set up with an editable install of the project package (step #3).

> Unit tests will fail if Step #3 of the DEVELOPER SETUP guide is skipped.

## Running unit tests

From the `tests/unit` directory:

**Run the full suite:**

```bash
pytest
```

**Run a single test file:**

```bash
pytest <filename>
```

Example:

```bash
pytest test_fileops.py
```

**Run a single test function** (useful when iterating on one case):

```bash
pytest test_fileops.py::test_function_name
```

## Model tests

Not yet implemented. The `tests/model/` subdirectory is reserved for
tests that exercise the trained classifiers against held-out data and
reproducibility benchmarks. This section will be filled in once those
tests land.
