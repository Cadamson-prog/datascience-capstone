# TIDY / DATA PREP

__Notebook Authors__

- `create_main_data.ipynb` Kristin Predeck
- `NFI_data_load_and_merge.ipynb` Kristin Predeck

__Goals:__

- Load raw data files & convert file format as needed
- Get data into tidy/wide format for data exploration
- Confirm uniqueness of observations
- Preliminary data cleaning

__Key Decisions / Insights:__

- NFI = primary dataset due to high volume of particle data evenly distributed between GSR & Non-GSR target label.
- NIST is 30+ zipped file downloads, requires special Julia software for unpacking "Zeppelins", and data concatenation will take extra time. Complex dataset, potentially available for cross-test validation.

# Exploratory Data Analysis (EDA)

__Notebook Authors w/ estimated run time:__

- `particle_eda.ipynb` Kristin Predeck ~2 min
- `umap.ipynb` Brendan OConnell ~10 min

__Goals:__

- Explore data relationships & patterns
- Visually analyze key characteristics (correlations, distributions, interactions, etc.)
- Compare results of linear vs. non-linear methods
- Check for potential outliers / confounders / problematic features
- Identify class imbalances, target distributions, and leakages

__Key Decisions / Insights:__

- Reduce element features from original 89 to just the informative 27 elements. The other 62 elements appear to be noise, offering near-zero value.
- UMAP vs PCA comparison suggests strong non-linear relationships.
- Ambiguous particles cannot confidently be classified as either GSR or Non-GSR.
- Non-GSR barium particle classes will likely be high contributors to false positives.

# Feature Processing

### Preprocessing

__Notebook Authors:__

- `pipeline.ipynb` Brendan OConnell
- `pipeline_minimal_xgb.ipynb` Brendan OConnell

__Goals:__

- Transform data into "ML-ready" state
- Scale / Normalize data as needed
- Target encoding
- Determine how to handle outliers (not applicable)
- Handle missing data (not applicable)

__Key Decisions__

- Drop ambiguous particle classes from main dataset
- Apply binary target label to remaining particles (GSR vs. Non-GSR)

### Feature Engineering

__Notebook Authors w/ estimated run time:__

- `feature_exploration_xgboost.ipynb` Brendan OConnell ~25s
- `feature_exploration_nn.ipynb` Kristin Predeck ~40s
- `feature_exploration_log_regression.ipynb` Carlos Adamson ~80s

__Goals:__

- Create predictive signal
- Domain features
- Interaction features
- Feature selection
- Identify class imbalances, target distributions, and leakages

__Key Decisions / Insights__

- Elemental ratios require special attention and consideration for risk of introducing bias when denominator is 0
- `NaN` and `inf` arise with 0 in denominator. Different approaches were experimented with (epsilon vs. sentinel vs. total mass denominator)

# Model Exploration

__Notebook Authors w/ estimated run time:__

- `Logisitic_Regression.ipynb` Carlos Adamson ~1 min
- `xgboost_baseline_v2.ipynb` Brendan OConnell ~4 min
- `nn_baseline_v2.ipynb` Kristin Predeck ~27 min

__Goals:__

- Split: train set / test set / validation set
- Identify promising model candidates
- Establish baselines
- Compare model performance metrics
- Process of elimination

__Outputs:__

- Baseline Models

# Model

__Notebook Authors w/ estimated run time:__

- `xgb_optimize.ipynb` Brendan OConnell ~6 min
- `nn_tuning.ipynb` Kristin Predeck *TBD* (>20min)
- `HP_Logistic_Regression.ipynb` Carlos Adamson *TBD* (>20min)

__Goals:__

- Optimize the chosen model
- Hyperparameter tuning
- Cross validation (e.g. kNN)
- Final training

__Output:__

Production-ready models

# Evaluation

__Notebook Authors w/ estimated run time:__

- `nn_ablation_study.ipynb` Kristin Predeck ~3.5 min
- `xgb_eval_v2.ipynb` Brendan OConnell ~5 min

__Goals:__

- Interpret model behavior
- Failure Analysis

# Validation

__Notebook Authors w/ estimated run time:__

- `xgb_nist_validation.ipynb` Brendan OConnell ~4 min
- `logistic_regression_nist_validation.ipynb` Carlos Adamson *TBD* (long)
- `NN_nist_validation.ipynb` Carlos Adamson *TBD* (long)

__Goals:__

- Cross-test w/ NIST
- Interpret model behavior w/ NIST
- Failure Analysis w/ NIST

# Supplementary Notebooks

> These notebooks are not included in the "validate notebook" scripts because they are not considered part of the main DataScience Flow.

## Presentation

__Notebooks w/ estimated run time:__

- `xgb_vs_nn.ipynb` ~5s
- `pca_vs_umap.ipynb` ~4 min
- `overfitting_ablation_ambiguous.ipynb` ~24 min

These "presentation" notebooks utilize code from previous notebooks to redesign, enhance, or create new visuals. **All authors are credited here.**

__Goals:__

- Compare key model behaviors side-by-side (e.g., PCA vs UMAP, XGBoost vs NN)

__Outputs:__

- Polished visualizations for the final report and presentation

## Sandbox

> These are kept for traceability/historical context and are not maintained against the latest data layouts.

__Notebook Authors w/ estimated run time:__

- `data_prep/NIST_data_inspect.ipynb` Kristin Predeck *TBD*
- `eda/EPA_environmental_confounder_analysis.ipynb` Carlos Adamson *TBD*
- `eda/NFI_oxygen_analysis.ipynb` Brendan OConnell ~30s
- `eda/particle_eda_viz_formatting.ipynb` Kristin Predeck ~2 min (just a copy of her EDA notebook w/ added viz formatting)
- `eda/oxygen.ipynb` Brendan OConnell ~24s
- `model_baseline_exploration/nn_baseline.ipynb` Kristin Predeck ~13 min
- `model_baseline_exploration/xgboost_baseline_v1.ipynb` Brendan OConnell ~1.5 min
- `model_baseline_exploration/xgboost_baseline_v3.ipynb` Brendan OConnell ~3 min
- `model_baseline_exploration/xgboost_baseline_v4_no_eng_feats.ipynb` Brendan OConnell ~4 min
- `model_eval/xgb_eval.ipynb` Brendan OConnell ~6 min
- `model_eval/xgb_eval_v3.ipynb` Brendan OConnell *TBD*
- `validation/renormalize_NIST_oxygen.ipynb` Brendan OConnell ~6s

__Goals:__

- Exploratory and experimental notebooks that are not part of the main DS Flow
- Alternative/failed/unchosen model iterations preserved for reference
- One-off investigations
