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

# Model Exploration

__Goals:__

- Split: train set / test set / validation set
- Identify promising model candidates
- Establish baselines
- Compare model performance metrics
- Process of elimination

# Model

__Goals:__

- Optimize the chosen model
- Hyperparameter tuning
- Cross validation
- Final training

__Output:__

Production-ready model

# Evaluation

__Goals:__

- Interpret model behavior
- Failure Analysis

# Validation

__Goals:__

- Cross-test w/ NIST
- Interpret model behavior w/ NIST
- Failure Analysis w/ NIST