

# Machine Learning for Gunshot Residue (GSR) Classification<br><br>*Accuracy, Interpretability, and Failure Analysis*
____________________________________________________________
> Join the conversation! Checkout our [Discussion Board](https://github.com/bkoconnell/datascience-capstone/discussions) where we brainstorm and collaborate on the project.
____________________________________________________________

Read our [docs/](https://github.com/bkoconnell/datascience-capstone/tree/main/docs) for __*developer setup*__ (reproducibility), __*contributing*__ guidelines, and general support documentation.

## Table of Contents
- [Team Delta](#team-delta)
- [Project Background](#project-background)
- [Research Questions](#research-questions)
- [Hypotheses & Predictions](#hypotheses--predictions)
- [Stakeholders](#stakeholders)
- [Data](#data)
- [Methods](#methods)
- [Technical Stack](#technical-stack)
- [Model Testing & Reproducibility](#model-testing--reproducibility)
- [Repository Structure](#repository-structure)
- [Project Timeline](#project-timeline)

## Team Delta

*Official team member accounts are listed in [CODEOWNERS](https://github.com/bkoconnell/datascience-capstone/blob/main/CODEOWNERS)*

### Project Attributions

__EDA__
- NFI (primary dataset): **Kristin Predeck**
- NIST (secondary dataset): **Brendan OConnell**
- EPA Environmental Confounders (secondary dataset): **Carlos Adamson**

__Models__
- Logistic Regression: **Carlos Adamson**
- XGBoost: **Brendan OConnell**
- Neural Net: **Kristin Predeck**

> NOTE: Individual file attributions can be found in the file headers with Author details.

### Peer Reviews

We rely on the following resources for our peer reviews:

- Pull Request comments (for non-notebook files, general feedback, and PR approvals)
- Our [GitNotebooks](https://app.gitnotebooks.com/bkoconnell/datascience-capstone/pulls) page (3rd party resource specifically for Jupyter Notebook reviews)

__*GitNotebooks*__ addresses the shortcomings of GitHub's UI, which displays `.ipynb` files as raw JSON and is not conducive to interpretable reviews. Here is an example of a PR review our team recently did: [PR-47 Peer Review](https://app.gitnotebooks.com/bkoconnell/datascience-capstone/pull/47)

## Project Background

Gunshot residue (GSR) analysis is a critical component of forensic investigations involving firearm discharge. When a firearm is fired, microscopic particles containing elements such as lead (Pb), barium (Ba), and antimony (Sb) are released and can serve as key physical evidence in criminal cases. Traditional GSR identification relies on scanning electron microscopy with energy dispersive X-ray spectroscopy (SEM/EDS), where expert analysts classify particles based on morphology and elemental composition.

However, this process is prone to error. Chemically similar particles from environmental sources, such as brake dust, fireworks, and industrial materials, can produce false positives, while atypical GSR compositions may lead to false negatives. Since interpretation depends heavily on expert judgment, consistency and reproducibility across analyses remain concerns, particularly in high-stakes legal contexts.

Machine learning offers a data-driven alternative that can improve the consistency, scalability, and transparency of GSR classification. Unlike prior work that focuses primarily on model accuracy and efficiency, this project emphasizes interpretability and failure analysis. Understanding *why* models make decisions and *where* they fail is essential for responsible application in forensic science.

## Research Questions

1. **Primary:** How accurately and reliably can machine learning models distinguish true gunshot residue particles from chemically similar non-GSR particles?
2. **Comparative:** How does classification performance vary across different machine learning approaches (linear, tree-based, neural network) when applied to GSR identification?
3. **Interpretability:** Which elemental features and combinations contribute most strongly to model predictions, and how consistent are feature importance patterns across models?
4. **Failure Analysis:** Under what conditions do models misclassify particles, particularly false positives where environmental particles are incorrectly labeled as GSR, and what does this reveal about the limitations of automated classification?

## Hypotheses & Predictions

### Hypotheses

- Machine learning models can effectively distinguish true GSR particles from environmental confounders, with performance depending on algorithm choice and the underlying chemical characteristics of particles.
- Non-linear models (e.g., gradient-boosted trees, neural networks) will outperform linear models (e.g., logistic regression) due to complex interactions among elemental features.
- Particles lacking the classic Pb-Ba-Sb signature are more likely to be misclassified as false negatives, while chemically similar confounders such as brake dust will drive higher false positive rates.

### Predictions

- Non-linear models will outperform the logistic regression baseline across accuracy, precision, recall, F1 score, and ROC-AUC, though hyperparameter tuning will be necessary to reduce false positive rates for chemically ambiguous particles.
- Feature importance analyses (e.g., SHAP, permutation importance) will identify lead, barium, and antimony — and their ratios — as the most influential predictors, especially in borderline classifications.
- Misclassifications will concentrate among particles with elemental profiles that partially overlap with the Pb-Ba-Sb signature, highlighting edge cases that would benefit from additional expert review rather than fully automated classification.

## Stakeholders
 
This research is relevant to a range of stakeholders across the forensic science and criminal justice landscape:
 
- **Crime laboratories and law enforcement agencies** (e.g., FBI Laboratory, ATF, state police crime labs) who would benefit from faster, more consistent GSR classification tools that reduce analyst workload and inter-examiner variability.
- **Standards and metrology bodies** (e.g., NIST, ENFSI) with an interest in developing validated, reproducible benchmarks for forensic particle analysis.
- **Legal and public defense organizations** (e.g., the Innocence Project, public defender offices) who have a stake in understanding false positive rates and model limitations, given the role forensic evidence plays in wrongful convictions.
- **Federal research funders** (e.g., the National Institute of Justice, NSF) who actively support research aimed at improving the scientific rigor of forensic methods.
 
## Data
 
This project uses two complementary datasets:
 
### NFI Gunshot Residue Dataset (Matzen et al., 2022)
- **Source:** Netherlands Forensic Institute ([GitHub](https://github.com/NetherlandsForensicInstitute/gunshot-residue))
- **Contents:** SEM/EDS particle measurements with expert-assigned relevance classes across four relational tables (stub, particle, source, stub_source)
- **Size:** 2,801,667 particles across 90 elemental composition columns from 210 criminal cases and 63 R&D projects
- **Role in this project:** Primary dataset for ML training and evaluation. Particles are labeled as GSR (1,078,946), Non-GSR (1,216,039), or Ambiguous (506,682) based on their merged relevance class, validated against NIST ground truth.

### NIST Gunshot Residue Dataset (Ritchie & Reynolds, 2021)
- **Source:** National Institute of Standards and Technology ([DOI: 10.18434/mds2-2660](https://www.nist.gov/glossary-term/38706))
- **Role in this project:** Used to validate NFI particle class labels by confirming which classes represent true GSR vs environmental confounders.
- **Files used:**

| File | Category | Particles | Data Available |
|------|----------|-----------|----------------|
| Shooter #1 - Zero time.zip | GSR (shooter hands) | 3,462 | Per-particle class labels from MLLSQ_maxParticle.csv |
| Shooter #2 - Zero time.zip | GSR (shooter hands) | 3,429 | Per-particle class labels from MLLSQ_maxParticle.csv |
| Sparklers post handling post burn.zip | Fireworks confounder | -- | HDZ class definitions only (no per-particle CSV) |
| Spinners - Post-ignition.zip | Fireworks confounder | -- | HDZ class definitions only |
| Roman Candles - Post-handling, pre-ignition.zip | Fireworks confounder | -- | HDZ class definitions only |
| Ford Explorer Rear Driver.zip | Brake dust confounder | -- | HDZ class definitions only |

- **Key finding:** NIST shooter samples confirmed that PbBaSb, PbBa, PbSb, and BaSb classes are genuine GSR. NIST confounder samples (fireworks, brake dust) lack GSR particle classes, confirming these are true environmental sources. This informed the labeling scheme applied to the NFI dataset.

### Labeling Scheme (NIST-Informed)

| NFI Class | Label | NIST Justification |
|-----------|-------|--------------------|
| PbBaSb | GSR | NIST: Classic GSR (GSR.0, GSR.1, GSR.2) |
| PbBa | GSR | NIST: GSR.Pb-Ba |
| PbSb | GSR | NIST: GSR.Pb-Sb |
| BaSb | GSR | NIST: GSR.Ba-Sb |
| BaAl, BaCaSi | Non-GSR | No NIST GSR equivalent |
| CuZn | Non-GSR | NIST: Brass -- environmental, not GSR |
| ZnTi, Hg, TiZnGd, GaCuSn | Non-GSR | Environmental particles |
| Pb, Ba, Sb, Sr | Ambiguous | Single-element -- could be GSR fragment or environmental |

## Methods

### Preprocessing
- Merged 14 NFI particle files with corrected headers (files 2–14 lacked column names)
- Applied NFI documentation merging rules to consolidate relevance classes
- Assigned NIST-informed binary labels (GSR vs Non-GSR)
- Identified 90 elemental composition columns as features
 
### Models
| Model | Type | Purpose |
|---|---|---|
| Logistic Regression | Linear | Baseline classifier to establish a performance floor |
| XGBoost | Tree-based (nonlinear) | Capture complex feature interactions |
| Fully Connected Neural Network | Deep learning (tabular) | Test deep learning on structured elemental data |

All hyperparameter tuning will be oriented toward minimizing false positives while maintaining low false negatives. Dimensionality reduction (PCA for linear space, UMAP for nonlinear space) will be explored selectively on the NFI elemental features (Ac–Zr), but only where it does not compromise interpretability.
 
### Evaluation
- **Classification metrics:** Accuracy, precision, recall, F1 score, ROC-AUC, and Precision-Recall AUC (to account for expected class imbalance)
- **Specificity focus:** False positive rate is central — incorrectly labeling a non-GSR particle as GSR represents a critical failure mode
- **Confusion matrices:** Used extensively to investigate misclassification patterns
- **Validation:** Cross-validation across folds; cross-dataset validation (train on NFI, test on NIST) to assess real-world generalizability
 
### Interpretability
- **Feature importance:** SHAP values and permutation importance to quantify the influence of elemental concentrations and ratios on predictions
- **Integrated gradients:** Probe neuron activation based on input features in neural network models
- **Spectral contribution:** Analyze contribution scores for spectral peaks in image-derived features
- **Goal:** Transform traditionally "black box" models into interpretable tools suitable for forensic contexts
 
### Misclassification Analysis
- Identify patterns in elemental composition or spectral features that drive false positives and false negatives
- Pay particular attention to chemically similar particles and edge cases that warrant expert review
- Inform both model limitations and practical forensic implications of automated GSR classification
 
## Technical Stack
 
- **Language:** Python
- **Core libraries:** pandas, numpy, scikit-learn, xgboost, pytorch
- **Visualization:** matplotlib, seaborn
- **Interpretability:** shap
- **Version control:** Git / GitHub / Git LFS (large file storage for parquets)
- **Formatting:** Ruff

## Model Testing & Reproducibility

### Model Testing

The latest model releases are found here: `artifacts/models/`.

Pre-designed tests for the latest model releases are available in `tests/model/`.

> TODO: Write model tests. Then add steps here for running the Model Tests

### Test Automation (GitHub)

CI runs on every pull request to `main` (and on manual dispatch) via GitHub Actions in [.github/workflows/](.github/workflows/). The pipeline is composed of the following jobs:

- **Python Lint** — Runs Ruff in format-check mode against the repo's Python sources. Fails the PR if any file is not ruff-format-clean and uploads the proposed diff as a build artifact.
- **Notebook Lint** *(not released)* — Will enforce notebook hygiene (cleared outputs, consistent formatting, etc.) so that `.ipynb` reviews on GitNotebooks stay focused on substantive changes.
- **Unit Tests** — Runs the `pytest` suite under `tests/unit/` against a freshly installed environment (`pip install -r requirements.txt` + editable install of the project package).

Non-PR automation jobs:
- **Reproducibility** *(not released)* — Users can manually trigger this workflow for an end-to-end data and modeling pipeline on a slim sample so that downstream notebooks remain runnable from a clean clone.

### Local Reproducibility

> **Prerequisite:** Follow [docs/DEVELOPER_SETUP.md](docs/DEVELOPER_SETUP.md) to set up Python, the virtual environment, and Git LFS so the project's data and dependencies resolve correctly.

The [src/](src/) directory hosts reusable Python code (helpers, model utilities, scripts) that the notebooks import. Centralizing logic there keeps notebooks focused on narrative and exploration while letting non-trivial functions be shared, tested, and lint-checked alongside the rest of the codebase.

### Local Testing

> **Prerequisite:** Follow [docs/DEVELOPER_SETUP.md](docs/DEVELOPER_SETUP.md) before running the steps below.

**Lint** — From the repository root, run the wrapper that matches your shell. Both forward to `src/scripts/linting/py_lint.py` and apply Ruff formatting in place:

```bash
# macOS / Linux
./lint.sh

# Windows
lint.bat
```

Inspect the resulting diff and commit any changes the formatter applies; the CI `Python Lint` job will fail otherwise.

**Unit tests** — From the `tests/unit/` directory, run the full suite or a single file:

```bash
# Run all unit tests
pytest

# Run a specific test file
pytest test_fileops.py
```

See [tests/README.md](tests/README.md) for additional usage details.

## Repository Structure
 
```
datascience-capstone/
├── .github/
│   └── workflows/                  # CI workflows (py-lint, nb-lint, unit-tests)
├── artifacts/
│   ├── models/                     # Trained model artifacts (e.g., neural_network/)
│   └── reports/                    # Submitted reports
│       ├── 01_eda/
│       ├── 02_feature_processing/
│       └── 03_model_exploration/
├── data/
│   ├── raw/                        # Original unmodified datasets
│   │   ├── NFI/                    # primary dataset
│   │   └── NIST/                   # secondary dataset
│   │
│   └── processed/                  # Team Delta's cleaned/engineered output files
│       │
│       ├── particle_labeled.parquet             # Full NFI dataset for EDA
│       ├── particle_ambiguous.parquet           # Subset of NFI w/ only Ambiguous particles
│       ├── preprocessed.parquet                 # Post-EDA NFI w/ 27 Elements and w/o Ambiguous
│       ├── preprocessed_minimal.parquet         # Post-EDA NFI w/ 89 elements and w/o Ambiguous
│       ├── engineered_features_logistic.parquet # NFI Feature Engineered (log reg)
│       ├── engineered_features_xgboost.parquet  # NFI Feature Engineered (xgb)
│       ├── engineered_features_nn.parquet       # NFI Feature Engineered (nn)
│       │
│       ├── preprocessed_nist.parquet            # NIST for cross-testing
│       └── nist_concatenated_parquets/          # NIST concatenated (not fully processed)
│ 
├── docs/                           # Project documentation, reports, and references
│   ├── CLONING.md
│   ├── CONTRIBUTING.md
│   ├── DEVELOPER_SETUP.md
│   ├── python_setup.md
│   ├── data_dictionaries/          # Per-stage data dictionaries
│   └── workflows/                  # Linting and testing workflow docs
│ 
├── notebooks/                      # Jupyter Notebooks for the DataScience Flow
│   │                                (w/ ephemeral `outputs/` dir per section)
│   ├── 00_tidy_data_prep/
│   ├── 01_eda/
│   ├── 02_feature_processing/
│   ├── 03_model_exploration/
│   ├── 04_model/
│   ├── 05_evaluation/
│   ├── 06_presentation/
│   └── 99_sandbox/
├── src/                            # Reusable Python source supporting notebooks
│   ├── eda.py
│   ├── exceptions.py
│   ├── scripts/                    # Standalone data-prep / lint scripts (incl. julia/)
│   └── utils/                      # Shared helpers: common, fileops, logreg, nist, nn, xgb
├── tests/                          # Pytest suite
│   ├── model/                      # Model tests (TODO — not yet implemented)
│   └── unit/                       # Unit tests for src/ helpers + lint script
├── lint.bat / lint.sh              # Local lint entrypoints (Ruff)
├── pyproject.toml                  # Project + tooling configuration
└── requirements.txt                # Python dependencies
```
 
## Project Timeline
 
| Week | Focus | Deliverable |
|---|---|---|
| 1 | Team formation, topic selection, define objectives and scope | Project Proposal |
| 2 | Data sourcing, cleaning, and finalize analysis plan | Data Acquisition and Exploration Report |
| 3 | Exploratory data analysis, visualizations, and summary statistics | — |
| 4 | Handle missing values and outliers, feature scaling and engineering | Data Preprocessing and Feature Engineering Report |
| 5 | Select ML algorithms, validate assumptions, build initial models | Model Selection and Development Report |
| 6 | Cross-validation, hyperparameter tuning, and model evaluation | Model Evaluation and Interpretation Report |
| 7 | Interpret results, failure analysis, and visual storytelling | — |
| 8 | Final presentations and submit all written deliverables and code | Capstone Project Final Report |
