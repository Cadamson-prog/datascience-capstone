# 📊 Feature Engineering Tables – Logistic Regression

## Overview
This folder describes the key tables generated in the logistic regression feature engineering notebook. These tables support validation, interpretability, and reproducibility of the engineered dataset used for downstream modeling.

---

## 1. Feature Set Summary Table

**Purpose:**  
Provides a structured view of the different feature tiers created for model comparison.

**Tables Included:**
- `full_features`
- `engineered_only_features`
- `extreme_drop_features`

**Description:**
- **Full Features**  
  Includes all original elemental features (e.g., Pb, Ba, Sb) along with engineered transformations such as ratios, interactions, and normalized compositions.
  
- **Engineered-Only Features**  
  Removes direct elemental indicators that strongly proxy the label and retains only derived features (ratios, interactions, normalized values).
  
- **Extreme Drop Features**  
  Excludes all features containing Pb, Ba, or Sb to test whether the model can generalize using secondary chemical patterns.

**Use Case:**  
Supports controlled model comparisons and helps evaluate reliance on domain-defining elements.

---

## 2. Engineered Feature Validation Table

**Purpose:**  
Confirms that all expected engineered features were successfully created and categorized.

**Key Components:**
- Log-transformed features (`log_*`)
- Ratio features (`*_ratio`)
- Interaction features (`*_x_*`)
- Composition-normalized features (`*_pct`)
- Diversity metrics (e.g., element count)

**Description:**  
Acts as a checklist to ensure:
- No feature groups are missing  
- Naming conventions are consistent  
- Feature engineering logic executed correctly  

**Use Case:**  
Prevents silent errors before modeling and ensures reproducibility.

---

## 3. Feature Inclusion / Exclusion Table

**Purpose:**  
Documents which features are included or excluded across each feature tier.

**Description:**
- Identifies:
  - Features removed due to leakage risk (e.g., label proxies)  
  - Features excluded for stricter generalization tests  
  - Features retained for baseline performance  

**Use Case:**  
Critical for explaining modeling decisions in the final report and defending feature selection choices.

---

## 4. Statistical Distribution Summary Table

**Purpose:**  
Summarizes key descriptive statistics of engineered features.

**Metrics Included:**
- Mean  
- Median  
- Standard deviation  
- Min / Max  
- (Optional) Skewness or quantiles  

**Description:**  
Used to evaluate:
- Effects of log transformations  
- Reduction in skewness  
- Scaling consistency across features  

**Use Case:**  
Validates that features align with logistic regression assumptions (linearity in log-odds, reduced skew).

---

## 5. Class-Based Comparison Table

**Purpose:**  
Compares feature distributions between target classes (`GSR` vs `Non-GSR`).

**Description:**
- Highlights differences in:
  - Ratio features  
  - Interaction terms  
  - Normalized compositions  

**Use Case:**  
Provides early signal of feature separability and helps justify inclusion of engineered variables.

---

## 6. Correlation Summary Table

**Purpose:**  
Quantifies relationships between engineered features.

**Description:**
- Identifies:
  - Highly correlated features (potential multicollinearity)  
  - Redundant engineered features  
  - Independent predictors  

**Use Case:**  
Supports feature pruning and helps maintain stability in logistic regression coefficients.

---

## 7. Pre / Post Transformation Comparison Table

**Purpose:**  
Evaluates the impact of transformations (especially log scaling).

**Description:**
- Compares original vs transformed versions of key features  
- Highlights:
  - Reduced skewness  
  - Improved distribution symmetry  

**Use Case:**  
Demonstrates that preprocessing improves suitability for linear modeling.

---

## How These Tables Support Modeling

Together, these tables ensure that:
- Feature engineering is transparent and reproducible  
- Leakage is minimized  
- Logistic regression assumptions are respected  
- Model comparisons across feature tiers are defensible  

