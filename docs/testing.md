# Testing Locally

- [`tests/unit/`](../tests/unit/) - unit tests for source code in [`src/`](../src/).

### Prerequisites

Complete steps 1 & 2 in the [QuickStart](QuickStart.md) guide, or manually configure using the [DEVELOPER SETUP](DEVELOPER_SETUP.md) walkthrough to get your Python environment set up with an editable install of the project package.

## Running unit tests

From the **`tests/unit`** directory:

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
