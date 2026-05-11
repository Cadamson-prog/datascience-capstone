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

# 5. Run the new Notebook Validation Test via GitHub Actions!

A brand new CI job called `nb-validate` that you can manually trigger via GitHub Actions.

Validates the execution of our 18 primary notebooks. The most recent validation test was on 5/11 and all 18 notebooks ran from start to finish without any errors.

[View the results on our GitHub repo!](https://github.com/bkoconnell/datascience-capstone/actions/runs/25662999047)

The notebooks run in parallel. Timings vary considerably. You can view a complete list of notebooks and their estimated execution times for test in the **[nb-validate doc](https://github.com/bkoconnell/datascience-capstone/blob/main/docs/github_actions/nb_validate.md)**

**Our Recommendation** is to go to our [GitHub Actions - NB Validate](https://github.com/bkoconnell/datascience-capstone/actions/workflows/nb-validate.yml) page, click the `Run workflow` drop-down to the far right (it should default to `main` branch), then click the green **Run workflow** button to dispatch all 18 validation tests. 

Then go to step 6 while you wait for the results!

For your reference, the most recent Notebook Validation Test ran for 1hr 2min

---

# 6. Reproducibility Check

## Manually run our [notebooks/](https://github.com/bkoconnell/datascience-capstone/blob/main/notebooks)

While you're waiting for the GitHub CI test results from step 5, keep yourself busy by manually validating the notebooks to confirm reproducibility.

We recommend you first look at [NOTEBOOKS.md](https://github.com/bkoconnell/datascience-capstone/blob/main/notebooks/NOTEBOOKS.md), which lists estimated run times for each notebook, identifies the author of each notebook, and logically identifies which notebooks are not considered part of our primary DataScience Flow (hint: subdirectories `99_presentation`, `99_sandbox`, and `archived`).

All our primary notebooks in the DataScience Flow should execute fully without errors. This includes the following subdirectories in `notebooks/`:
- 01_eda
- 02_feature_processing
- 03_model_exploration
- 04_model
- 05_evaluation
- 06_validation

It does **not** include:
- 99_presentation
- 99_sandbox
- archive

Some of the `99_` notebooks may run but are not guarenteed as they sometimes require maintenance and do not get the same attention as our main flow. The `archived` notebooks do not run and are only saved for historical context.

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
