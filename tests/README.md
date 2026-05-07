The `tests` directory supports all testing functionality for the project. It is organized into two subdirectories:

- [`model/`](model/) — Model testing (see below).
- [`unit/`](unit/) — Unit tests for shared source code under [`src/`](../src/).

---

## Model Testing

> **TODO:** Model testing is not yet implemented. The [`model/`](model/) subdirectory is reserved for forthcoming tests that exercise the trained classifiers (logistic regression, XGBoost, neural network) against held-out data and reproducibility benchmarks.

---

## Unit Testing

__Prerequisites__

    - Follow the instructions in `docs/DEVELOPER_SETUP.md`

### Steps for running tests

__Run all unit tests:__

From the `tests/unit` directory, run:

    pytest

__Run a specific test:__

From the `tests/unit` directory, run:


    pytest <filename>

Example:

    pytest test_fileops.py
