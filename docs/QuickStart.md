# Quick Start guide in 7 steps

This is a streamlined guide for efficiently navigating through the project repository and validating our work.

### Prerequisites

Make sure you already ...

- **Cloned the repository** to your local machine (see [CLONING.md](CLONING.md))
- **Have a supported version of Python installed** (see [python_setup.md](python_setup.md)). Ideally 3.9+

---

> All commands below assume your terminal's **current working directory** is the **project root:** `datascience-capstone/`

---

# 1. Run the `devsetup` script

This automates the task of configuring your local environment to align with the project (skips the virtual environment step if you've already configured it, so running the devsetup script multiple times is safe).

**Windows (PowerShell):**
```powershell
.\devsetup.bat
```

**macOS / Linux / Git Bash:**
```bash
./devsetup.sh
```

**Alternatively**, follow the steps in the [DEVELOPER_SETUP.md](DEVELOPER_SETUP.md) to manually configure your local environment. However, running the devsetup script is the recommended (and fastest) approach.

---

# 2. Activate the Virtual Environment

If you ran the devsetup script or have deactivated the venv, you will need to ensure it is activated.

**Windows (PowerShell):**
```powershell
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

---

# 3. Run the `lint` script

Validate Python formatting compliance for .PY scripts and .IPYNB notebooks.

**Windows (PowerShell):**

```powershell
.\lint.bat
```

**macOS / Linux / Git Bash:**

```bash
./lint.sh
```

--

# 4. Run the `import-lint` script

Validate compliance with best practices for location of import statements in code files (scripts/notebooks).

**Windows (PowerShell):**

```powershell
python src\scripts\linting\import_lint.py
```

**macOS / Linux / Git Bash:**

```bash
python src/scripts/linting/import_lint.py
```

--

# 5. Run the `validate` script

Validate reproducibility of our [notebooks](https://github.com/bkoconnell/datascience-capstone/tree/main/notebooks). 

You always have the option to manually validate the notebooks. If so, we recommend you first look at [NOTEBOOKS.md](https://github.com/bkoconnell/datascience-capstone/blob/main/notebooks/NOTEBOOKS.md), which lists estimated run times for each notebook, identifies the author of each notebook, and logically identifies which notebooks are not considered part of our primary DataScience Flow (hint: subdirectories `99_presentation` and `99_sandbox`).

> If you choose to manually validate the notebooks, you can skip the rest of this step and move to **#6** when you've completed the validation. 
Otherwise, the details for running the `validate` script are below.

All relevant notebooks in the DataScience Flow should execute fully without errors. This includes the following subdirectories in `notebooks/`:
- 00_tidy_data_prep
- 01_eda
- 02_feature_processing
- 03_model_exploration
- 04_model
- 05_evaluation
- 06_validation

It does **not** include:
- 99_presentation
- 99_sandbox

> Running the validate script without the `--max_nb_runtime` option will run *all* notebooks listed above (excluding `99_` prefixed subdirectories), which will be very time consuming. Consider the `--max_nb_runtime` options below.

We have runtime estimates for our notebooks.
You can pass the `--max_nb_runtime` option to skip notebooks that we estimate to run over a certain amount of minutes. Here are the options:

- `--max_nb_runtime=5` (any NB with runtime over 5 minutes is skipped)
- `--max_nb_runtime=10` (and so on ...)
- `--max_nb_runtime=20`
- `--max_nb_runtime=30`

Validation runs 1 notebook at a time, not in parallel. Based on current runtimes, here are the estimated total execution times for validation per option:
- max_nb_runtime=5 ... **total estimated execution time =  __ minutes**
- max_nb_runtime=10 ... **total estimated execution time =  __ minutes**
- max_nb_runtime=20 ... **total estimated execution time =  __ minutes**
- max_nb_runtime=30 ... **total estimated execution time =  __ minutes**

We do not have a total estimated execution time for running the validate script without the `--max_nb_runtime` option.

**Windows (PowerShell):**

```powershell
.\validate.bat
```
or with max_runtime (recommended):
```powershell
.\validate.bat --max_runtime=5
```

**macOS / Linux / Git Bash:**

```bash
./validate.sh
```
or with max_runtime (recommended):
```bash
./validate.sh --max_runtime=5
```

---

# 6. Test a model

Not implemented yet.

---

# 7. Best Practices

Review our best practices matrix in the [CONTRIBUTING.md](CONTRIBUTING.md) doc to see how our project implementations align with requirements.

---

## Optional: Unit Tests for Custom Functions

Read [SOURCE.md](https://github.com/bkoconnell/datascience-capstone/blob/main/src/SOURCE.md) to learn more about our custom functions.

To run all unit tests for the custom functions, first **change directory** to **`tests/unit/`** then run this from the command line:

```
pytest
```

Or checkout the [testing](testing.md) documentation for more options.
