# TIDY / DATA PREP

__Goals:__

- Load raw data files & convert file format as needed
- Get data into tidy/wide format for data exploration
- Confirm uniqueness of observations
- Preliminary data cleaning

__Key Decisions:__

- NFI = primary dataset

__Reasoning:__

High volume of particle data evenly distributed between GSR & Non-GSR target label.

# Exploratory Data Analysis (EDA)

__Goals:__

- Explore data relationships & patterns
- Visually analyze key characteristics (correlations, distributions, interactions, etc.)
- Compare results of linear vs. non-linear methods
- Check for potential outliers / confounders / problematic features
- Identify class imbalances, target distributions, and leakages

__Key Decisions:__

- Reduce element features from original 89 to just the informative 27 elements

__Reasoning:__

62 of the original 89 elements offered zero informative values and instead were just noise. We've selected only the 27 elements that had informative input values.

__Notebooks (estimated run time):__

- `particle_eda.ipynb` — ~2 min
- `umap.ipynb` — ~10 min

# Feature Processing

### Preprocessing

__Goals:__

- Transform data into "ML-ready" state
- Scale / Normalize data as needed
- Encoding
- Determine how to handle outliers if applicable
- Strategize handling imbalance (class weights, stratification, etc.)
- Handle missing data if applicable

### Feature Engineering

__Goals:__

- Create predictive signal
- Domain features
- Interaction features
- Feature selection
- Identify class imbalances, target distributions, and leakages

__Notebooks (estimated run time):__

- `feature_exploration_xgboost.ipynb` — ~25s
- `feature_exploration_nn.ipynb` — ~40s
- `feature_exploration_log_regression.ipynb` — ~80s

# Model Exploration

__Goals:__

- Split: train set / test set / validation set
- Identify promising model candidates
- Establish baselines
- Compare model performance metrics
- Process of elimination

__Notebooks (estimated run time):__

- `Logisitic_Regression.ipynb` — ~1 min
- `xgboost_baseline_v2.ipynb` — ~4 min
- `nn_baseline_v2.ipynb` — ~27 min

# Model

__Goals:__

- Optimize the chosen model
- Hyperparameter tuning
- Cross validation
- Final training

__Output:__

Production-ready model

__Notebooks (estimated run time):__

- `xgb_optimize.ipynb` — ~6 min
- `nn_tuning.ipynb` — *TBD* (cell timeout at ~20 min during HP grid search)
- `HP_Logistic_Regression.ipynb` — *timed out* (>33 min)

# Evaluation

__Goals:__

- Interpret model behavior
- Failure Analysis

__Notebooks (estimated run time):__

- `nn_ablation_study.ipynb` — ~3.5 min
- `xgb_eval_v2.ipynb` — ~5 min

# Validation

__Goals:__

- Cross-test w/ NIST
- Interpret model behavior w/ NIST
- Failure Analysis w/ NIST

__Notebooks (estimated run time):__

- `xgb_nist_validation.ipynb` — ~4 min
- `logistic_regression_nist_validation.ipynb` — *TBD*
- `NN_nist_validation.ipynb` — *TBD*

# Presentation

__Goals:__

- Distilled, polished visualizations for the final report and presentation
- Compare key model behaviors side-by-side (e.g., PCA vs UMAP, XGBoost vs NN)
- Tell the project's story with publication-quality figures

__Notebooks (estimated run time):__

- `xgb_vs_nn.ipynb` — ~5s
- `pca_vs_umap.ipynb` — ~4 min
- `overfitting_ablation_ambiguous.ipynb` — ~24 min

# Sandbox

__Goals:__

- Exploratory and experimental notebooks that are not part of the main pipeline
- Earlier model iterations preserved for reference
- One-off investigations

> NOTE: These are kept for traceability and historical context — they are not maintained against the latest data layouts.

__Notebooks (estimated run time):__

- `validation/renormalize_NIST_oxygen.ipynb` — ~6s
- `eda/oxygen.ipynb` — ~24s
- `eda/NFI_relevant_elements_only.ipynb` — ~30s
- `model_baseline_exploration/xgboost_baseline_v1.ipynb` — ~1.5 min
- `eda/particle_eda_viz_formatting.ipynb` — ~2 min
- `model_baseline_exploration/xgboost_baseline_v3.ipynb` — ~3 min
- `model_baseline_exploration/xgboost_baseline_v4_no_eng_feats.ipynb` — ~4 min
- `model_eval/xgb_eval.ipynb` — ~6 min
- `model_baseline_exploration/nn_baseline.ipynb` — ~13 min
- `data_prep/NIST_data_inspect.ipynb` — *TBD*
- `eda/EPA_environmental_confounder_analysis.ipynb` — *TBD*
- `model_eval/xgb_eval_v3.ipynb` — *TBD*