_Data Science Capstone (Team Delta)_

> See the [docs/](docs/) directory for support documentation and guidelines for contributing.

# Machine Learning for Gunshot Residue Classification: Accuracy, Interpretability, and Failure Analysis

## Table of Contents
- [Background](#background)
- [Questions](#questions)
- [Hypotheses & Predictions](#hypotheses--predictions)
- [Stakeholders](#stakeholders)
- [Data](#data)
- [Methods](#methods)
- [Technical Stack](#technical-stack)
- [Repository Structure](#repository-structure)
- [Project Timeline](#project-timeline)
- [Contributors](#contributors)

## Background

Gunshot residue (GSR) analysis is a critical component of forensic investigations involving firearm discharge. When a firearm is fired, microscopic particles containing elements such as lead (Pb), barium (Ba), and antimony (Sb) are released and can serve as key physical evidence in criminal cases. Traditional GSR identification relies on scanning electron microscopy with energy dispersive X-ray spectroscopy (SEM/EDS), where expert analysts classify particles based on morphology and elemental composition.

However, this process is prone to error. Chemically similar particles from environmental sources, such as brake dust, fireworks, and industrial materials, can produce false positives, while atypical GSR compositions may lead to false negatives. Since interpretation depends heavily on expert judgment, consistency and reproducibility across analyses remain concerns, particularly in high-stakes legal contexts.

Machine learning offers a data-driven alternative that can improve the consistency, scalability, and transparency of GSR classification. Unlike prior work that focuses primarily on model accuracy and efficiency, this project emphasizes interpretability and failure analysis. Understanding *why* models make decisions and *where* they fail is essential for responsible application in forensic science.

## Questions

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

### Processed Output
- `processed/particle_labeled.parquet` -- Full NFI dataset with added `final_class`, `label`, and binary `target` columns
- Generated by `notebooks/01_data_preparation.ipynb`

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
 
## Methods
 
### Preprocessing
- Standardize elemental concentration units and scales across both datasets
- Assess and handle missing values (imputation or removal as appropriate)
- Extract numerical features from TIFF spectral images for use in image-based modeling
- Engineer additional features such as elemental ratios (e.g., Pb/Ba, Sb/Ba)
 
### Models
| Model | Type | Purpose |
|---|---|---|
| Logistic Regression | Linear | Baseline classifier to establish a performance floor |
| XGBoost | Tree-based (nonlinear) | Capture complex feature interactions |
| Fully Connected Neural Network | Deep learning (tabular) | Test deep learning on structured elemental data |
| CNN (if feasible) | Deep learning (image) | Leverage spectral information from TIFF images |
 

## Stakeholders
 
- **Courts and legal decision-makers** who require GSR analysis to support judicial outcomes. Results must be accurate, reliable, reproducible, and interpretable to be admissible and trustworthy.
- **Expert witnesses and forensic analysts** who may use this pipeline as a starting point for deeper investigation. Transparency and ease of use are paramount to support existing workflows and aid in preparing expert testimony.
- **Defendants and defense counsel** who are directly impacted by classification errors. False positives are a critical concern, and defense teams may scrutinize failure modes and model limitations to ensure fair and transparent application of ML in forensic evidence.
- **Federal research funders** (e.g., the National Institute of Justice, NSF) who actively support research aimed at improving the scientific rigor of forensic methods.
 
## Data
 
This project uses two complementary datasets. Across both, the target variable is a binary indicator of GSR versus non-GSR: `gsr_label` in the NIST data and `merged_relevance_class` in the NFI data. Predictor variables consist primarily of elemental compositions (chemical signatures), along with ammunition type, case type, and TIFF spectral images (NIST only) as a secondary modality.
 
### NIST Gunshot Residue Dataset (Ritchie & Reynolds, 2021)
- **Source:** National Institute of Standards and Technology
- **Contents:** Particle-level SEM/EDS measurements including elemental concentrations (Pb, Ba, Sb, etc.), sample metadata, and TIFF images with embedded X-ray spectra
- **Size:** 30 discrete samples — 8 GSR, 12 brake dust, 10 fireworks
- **Collection:** Samples collected by the Boston Police Department from a volunteer at a firing range
- **Strengths:** High-quality, verified ground truth labels; suitable for benchmarking
- **Limitations:** Small sample size; single volunteer and collection setting limits generalizability
 
### NFI Gunshot Residue Dataset (Matzen et al., 2022)
- **Source:** Netherlands Forensic Institute (publicly available via GitHub)
- **Contents:** SEM/EDS particle measurements with classification labels across four relational tables (stub, particle, source, stub-source)
- **Size:** 1,953 samples from 210 criminal cases across ~964,000 particles
- **Collection:** Sampled from a variety of locations and case types between 2015–2019
- **Strengths:** Scale and diversity across real-world criminal cases; designed for ML analysis
- **Limitations:** Batch effects from multiple case types; limited elemental scope may miss edge-case confounders
 
## Methods
 
### Preprocessing
- Clean and standardize data: assess missing values (impute or drop), standardize units and scales of elemental concentrations across NIST and NFI datasets
- Extract numerical features from TIFF spectral images for use in image-based and combined modeling
- Engineer additional features such as elemental ratios and morphology descriptors where available
 
### Models
| Model | Type | Purpose | Key Hyperparameters |
|---|---|---|---|
| Logistic Regression | Linear | Baseline classifier and initial feature selection | Regularization strength |
| XGBoost | Tree-based (nonlinear) | Capture complex feature interactions | Tree depth, learning rate, number of estimators, class weighting |
| Fully Connected Neural Network | Deep learning (tabular) | Test deep learning on structured elemental data | Depth, hidden layer size, learning rate, batch size, dropout, early stopping |
| CNN (if feasible) | Deep learning (image) | Leverage spectral information from TIFF images | — |
 
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
- **Image processing:** opencv, tifffile
- **Version control:** Git / GitHub
 
## Repository Structure
 
```
datascience-capstone/
├── README.md
├── .gitignore
├── requirements.txt        # Python dependencies
├── data/
│   ├── raw/                # Original unmodified datasets
│   │   ├── NFI/            # NFI particle, stub, source CSVs (not tracked in git, file size too large)
│   │   └── NIST/           # NIST shooter, firework, brake dust zips (not tracked in git, file size too large)
│   └── processed/          # Cleaned and feature-engineered data
│       └── particle_labeled.parquet  # Full NFI dataset with labels and target
├── notebooks/              # Exploratory analysis and prototyping
│   ├── 01_data_preparation.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_modeling.ipynb
│   ├── 04_interpretability.ipynb
│   └── 05_failure_analysis.ipynb
├── src/
│   ├── preprocessing/      # Data cleaning and feature engineering scripts
│   ├── models/             # Model training and evaluation scripts
│   └── interpretability/   # SHAP, permutation importance, failure analysis
├── results/                # Model outputs, metrics, and visualizations
├── figures/                # Saved plots from notebooks
├── docs/                   # Project documentation, reports, and references
└── requirements.txt        # Python dependencies
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
 
## Contributors
 
- **Kristin Predeck**
- **Brendan OConnell**
- **Carlos Adamson**
