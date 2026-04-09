# Machine Learning for Gunshot Residue Classification: Accuracy, Interpretability, and Failure Analysis

## Exploratory Data Analysis Report

**Prepared by:** Kristin Predeck, Brendan OConnell, Carlos Adamson (Team Delta)

**Prepared for:** National Institute of Justice (Department of Justice research agency)

---

__A Note on Research Beneficiaries__

With the support of our primary funder, the National Institute of Justice, our findings aim to directly improve reliability and efficiency of GSR classification techniques for forensic science professionals in crime laboratories and law enforcement agencies, as well as metrology bodies like NIST who define benchmarks and standards for particle analysis. Additionally, public defenders and legal organizations such as the Innocence Project may find benefits from the results of our research, namely with false positive analysis and model limitations.

## 1. Background and Research Question

The identification of gunshot residue (GSR) particles is a cornerstone of forensic investigations involving firearm discharge. When a firearm is fired, microscopic particles containing characteristic elements such as lead (Pb), barium (Ba), and antimony (Sb) are deposited on nearby surfaces and can serve as physical evidence in criminal proceedings. Traditional GSR analysis relies on scanning electron microscopy with energy dispersive X-ray spectroscopy (SEM/EDS), a process that depends heavily on expert judgment and is susceptible to both false positives from chemically similar environmental particles and false negatives from atypical GSR compositions.

This project asks: **How accurately and reliably can machine learning models distinguish true gunshot residue particles from chemically similar non-GSR particles?** We further investigate how classification performance varies across model types (linear, tree-based, neural network), which elemental features drive predictions, and under what conditions models fail, particularly regarding false positives where environmental particles are incorrectly labeled as GSR.

## 2. Hypothesis and Prediction

We hypothesize that machine learning models can effectively distinguish true GSR particles from environmental confounders, with non-linear models (e.g., gradient-boosted trees, neural networks) outperforming linear models (e.g., logistic regression) due to the complex interactions among elemental features. We further hypothesize that particles lacking the classic Pb-Ba-Sb signature will be more prone to misclassification as false negatives, while chemically similar confounders will drive higher false positive rates.

We predict that feature importance analyses (e.g., SHAP, permutation importance) will identify lead, barium, and antimony, along with their ratios, as the most influential predictors, and that misclassifications will concentrate among particles with elemental profiles that partially overlap with the Pb-Ba-Sb signature.

## 3. Methods

### 3.1 Data Acquisition

This project draws on two complementary datasets:

1. **NFI Gunshot Residue Dataset** (Matzen et al., 2022): Sourced from the Netherlands Forensic Institute's public GitHub repository, this dataset contains SEM/EDS particle measurements from 210 criminal cases and 63 R&D projects. The data is distributed across four relational CSV tables (stub, particle, source, stub_source), with the particle data split across 14 separate CSV files. The dataset comprises 2,801,667 particles measured across 90 elemental composition columns. This serves as the primary dataset for model training and evaluation.

2. **NIST Gunshot Residue Dataset** (Ritchie & Reynolds, 2021): Obtained from the National Institute of Standards and Technology, this dataset provides ground-truth particle classifications from known shooter samples. Particle-level classifications were extracted from HDZ metadata files and MLLSQ_maxParticle.csv files. Two shooter samples (3,462 and 3,429 particles, respectively) were used to validate the labeling scheme applied to the NFI data. The NIST data was not merged into the training set but served as an external reference for label assignment.

### 3.2 Cleaning, Merging, and Aggregation

Several preprocessing steps were required before EDA could begin:

- First, the 14 NFI particle CSV files were concatenated into a single dataframe; files 2 through 14 lacked column headers, so the column names from file 1 were applied to all subsequent files.
- Second, the NFI documentation's merging rules were applied to consolidate the 27 original relevance classes into 15 final classes (e.g., PbSbBa, PbSbBaSn, and PbSbBaSr were all mapped to PbBaSb).
- Third, the NIST shooter samples were parsed to confirm which NFI particle classes correspond to genuine GSR. Based on this cross-referencing, each NFI particle was assigned one of three labels: GSR (classes PbBaSb, PbBa, PbSb, BaSb), Non-GSR (classes BaAl, BaCaSi, CuZn, ZnTi, Hg, TiZnGd, GaCuSn), or Ambiguous (single-element classes Pb, Ba, Sb, Sr that could represent either GSR fragments or environmental particles). 
- The particle data was then merged with the stub metadata table to enable analysis by sample source and project type. The final processed dataset was saved as a Parquet file for efficient downstream use.

We confirmed that there were no duplicate particle observations. The composite pairing of stub_id and particle_id yields zero duplicates for a total of 2,801,667 unique observations.

### 3.3 EDA Methods

Our exploratory analysis employed a combination of descriptive statistics, frequency tables, visualizations, and dimensionality reduction techniques. We chose these methods for the following reasons:

Descriptive statistics (means, proportions, non-zero rates) were computed for all 89 elemental features to characterize the distribution of each variable and identify which elements carry meaningful signal versus which are overwhelmingly zero. A sparsity analysis was conducted to separate "informative" elements (those with non-zero values in more than 1% of particles) from "sparse" elements, since the extreme sparsity of most elemental columns has direct implications for model selection. A bar chart of non-zero proportions per element was used to visualize this threshold.

A heatmap of mean elemental composition by particle class was generated to reveal the chemical signatures that distinguish different particle types. Stacked bar charts were used to assess class balance across the GSR, Non-GSR, and Ambiguous labels. A correlation matrix (correlogram) was computed for the informative elements within GSR particles specifically, to assess collinearity and identify element pairs that co-occur or inversely relate. Finally, Principal Component Analysis (PCA) was applied to the standardized informative features to explore whether linear dimensionality reduction could separate GSR from Non-GSR particles, and to examine where ambiguous particles fall in the reduced feature space. PCA loadings were inspected to determine which elements define the principal components.


## 4. Results

### 4.1 Dataset Overview

The processed dataset contains **2,801,667 particles** measured across **89 elemental composition features** (columns representing elements from Ac to Zr). Each particle also carries metadata columns: `stub_id`, `particle_id`, `relevance_class`, `merged_relevance_class`, `final_class`, and `label`.

**Table 1: Label Distribution**

| Label | Count | Proportion |
|---|---|---|
| Non_GSR | 1,216,039 | 43.4% |
| GSR | 1,078,946 | 38.5% |
| Ambiguous | 506,682 | 18.1% |

The dataset is reasonably balanced between GSR and Non-GSR classes. The 506,682 ambiguous particles (single-element classes such as Pb, Ba, Sb, and Sr) represent approximately 18% of the total and are excluded from the primary binary classification task, leaving 2,294,985 particles with a 47.0% GSR rate for model training and evaluation.

### 4.2 Sparsity Analysis

**Figure 1: Proportion of Particles with Non-Zero Values per Element** (see `particle_eda.ipynb`, Cell 7)

The sparsity analysis revealed that the vast majority of elemental columns are overwhelmingly zero. Of the 89 elemental features, only **27 elements** have non-zero values in more than 1% of particles. These "informative" elements are: O, S, Cu, Ba, Al, Si, Ca, Pb, Sb, Fe, Zn, Cl, K, Na, Mg, Ti, Sn, P, Mn, As, Cr, Br, Mo, Sr, Ni, W, and Hg. The remaining **62 elements** are extremely sparse (non-zero in fewer than 1% of particles) and carry minimal discriminative signal.

**Table 2: Informative vs. Sparse Element Counts**

| Category | Count | Examples |
|---|---|---|
| Informative (>1% non-zero) | 27 | O, S, Cu, Ba, Al, Si, Ca, Pb, Sb, Fe, Zn |
| Sparse (≤1% non-zero) | 62 | I, Zr, Bi, Gd, F, Ce, Er, Tc, Nd, Ge |

This extreme sparsity is an important characteristic of the data. It suggests that tree-based models, which naturally handle sparse features, may be well-suited for this classification task, while linear models and neural networks may require careful feature selection or dimensionality reduction.

### 4.3 Mean Elemental Composition by Particle Class

**Figure 2: Heatmap of Mean Elemental Composition (%) by Particle Class** (see `particle_eda.ipynb`, Cell 10)

The heatmap of mean elemental composition across the 15 final particle classes reveals distinct chemical signatures. The GSR-labeled classes (PbBaSb, PbBa, PbSb, BaSb) show elevated concentrations of lead, barium, and antimony in various combinations, consistent with the known chemistry of gunshot residue. Non-GSR classes exhibit markedly different profiles: BaCaSi particles are dominated by barium, calcium, and silicon; CuZn particles are characterized by copper and zinc (consistent with brass); and BaAl particles show high barium and aluminum content. The ambiguous single-element classes (Pb, Ba, Sb, Sr) show high concentrations of their namesake element but lack the multi-element signatures that would definitively classify them as GSR or non-GSR.

### 4.4 Class Balance

**Figure 3: Particle Count by Class (Stacked Bar Chart)** (see `particle_eda.ipynb`, Cell 12)

**Table 3: Final Class Distribution with Labels**

| Final Class | Label | Count |
|---|---|---|
| PbBaSb | GSR | 536,634 |
| CuZn | Non-GSR | 426,015 |
| BaCaSi | Non-GSR | 375,875 |
| BaAl | Non-GSR | 341,756 |
| PbBa | GSR | 236,299 |
| Sb | Ambiguous | 225,676 |
| PbSb | GSR | 196,294 |
| Pb | Ambiguous | 168,334 |
| BaSb | GSR | 109,719 |
| Ba | Ambiguous | 89,277 |
| ZnTi | Non-GSR | 44,530 |
| Sr | Ambiguous | 23,395 |
| TiZnGd | Non-GSR | 21,479 |
| Hg | Non-GSR | 4,750 |
| GaCuSn | Non-GSR | 1,634 |

The class distribution is uneven. PbBaSb (the classic three-component GSR) is the single largest class, while several Non-GSR classes (CuZn, BaCaSi, BaAl) are also well-represented. Some classes are quite small (GaCuSn with 1,634 particles, Hg with 4,750), which may affect per-class model performance. For the binary classification task (GSR vs. Non-GSR), the balance is approximately 47% GSR to 53% Non-GSR, which is favorable and unlikely to require aggressive resampling strategies.

### 4.5 Correlation Analysis (Collinearity Assessment)

**Figure 4: Element Correlations within GSR Particles (Correlogram)** (see `particle_eda.ipynb`, Cell 14)

**Table 4: Strongest Element Correlations among GSR Particles**

| Element 1 | Element 2 | Correlation |
|---|---|---|
| Zn | Cu | 0.535 |
| Pb | Ba | −0.407 |
| Ba | O | −0.361 |
| Sb | O | −0.301 |
| Na | S | 0.292 |
| Cu | O | −0.291 |
| Ca | Si | 0.280 |
| Pb | Al | −0.221 |
| Ba | Cu | −0.218 |
| Al | S | −0.216 |

The correlation matrix for informative elements within GSR particles reveals several notable patterns. The strongest positive correlation is between zinc and copper (r = 0.535), which is expected given that these elements co-occur in brass-related particles. Lead and barium show a moderate negative correlation (r = −0.407), suggesting that GSR particles tend to be enriched in one or the other rather than both simultaneously, which is consistent with the existence of distinct PbBa and PbSb subclasses. Several elements show negative correlations with oxygen (Ba, Sb, Cu), indicating that higher oxygen content is associated with lower concentrations of the key GSR signature elements. Calcium and silicon are positively correlated (r = 0.280), reflecting their co-occurrence in environmental mineral particles.

Overall, the correlations are moderate. No pair exceeds |r| = 0.54, suggesting that severe multicollinearity is not a major concern for the informative feature set. However, the Zn-Cu and Pb-Ba relationships should be monitored during modeling, as they may introduce redundancy in linear models.

### 4.6 PCA Visualization

**Figure 5: PCA Scatter Plots — GSR vs. Non-GSR and by Particle Class** (see `particle_eda.ipynb`, Cell 21)

**Figure 6: PCA Loadings for PC1 and PC2** (see `particle_eda.ipynb`, Cell 22)

**Figure 7: Ambiguous Particles in PCA Space** (see `particle_eda.ipynb`, Cell 25)

PCA was applied to the 27 informative elements (standardized via StandardScaler) for the binary subset (GSR and Non-GSR particles only). The first two principal components explain only **16.5% of the total variance** (PC1 = 8.5%, PC2 = 8.0%), and the scatter plots show substantial overlap between GSR and Non-GSR particles in this reduced two-dimensional space.

The PCA loadings reveal that PC1 is primarily driven by oxygen, sulfur, and barium (with opposing signs), while PC2 is influenced by copper, zinc, and iron. These loadings reflect the dominant chemical contrasts in the data but do not isolate the GSR-specific Pb-Ba-Sb signature into a single component.

When ambiguous particles (Pb, Ba, Sb, Sr classes) are projected into the same PCA space, they overlap heavily with both GSR and Non-GSR clusters, confirming that these single-element particles cannot be reliably separated using linear dimensionality reduction alone.

**Table 5: PCA Variance Explained**

| Component | Variance Explained |
|---|---|
| PC1 | 8.5% |
| PC2 | 8.0% |
| Total (PC1 + PC2) | 16.5% |

This result has important implications for model selection. The low variance explained by the first two principal components and the extensive overlap in PCA space indicate that linear models (such as logistic regression) will likely struggle to achieve strong classification performance. The discriminative information is distributed across many dimensions, and the relationships among elements are likely non-linear. This supports our hypothesis that non-linear models (gradient-boosted trees, neural networks) will be necessary to capture the complex feature interactions that distinguish GSR from non-GSR particles.


## 5. Discussion and Next Steps

### 5.1 Key Takeaways

The exploratory analysis reveals several findings that directly inform our modeling strategy and connect back to our research question about the reliability of ML-based GSR classification.

First, the data is extremely sparse: only 27 of 89 elemental features carry meaningful signal (Table 2, Figure 1). This sparsity, combined with the moderate correlations observed among informative elements (Table 4, Figure 4), suggests that tree-based models, which handle sparse inputs and feature interactions natively, are well-positioned for this task. The correlation analysis also confirms that while some element pairs co-occur (Zn-Cu) or inversely relate (Pb-Ba), severe multicollinearity is not present, meaning the informative features can be used together without aggressive dimensionality reduction.

Second, the PCA analysis (Figures 5–7, Table 5) demonstrates that linear dimensionality reduction captures only 16.5% of the variance in two components, and GSR and Non-GSR particles overlap substantially in this reduced space. This is a strong signal that the classification boundary is non-linear and high-dimensional, reinforcing our prediction that non-linear models will outperform logistic regression. The PCA results also show that ambiguous particles (Pb, Ba, Sb, Sr) are interspersed throughout the feature space, confirming that these single-element classes cannot be trivially assigned to either category and are appropriately excluded from the primary binary classification.

Third, the class balance is favorable for the binary task (47% GSR vs. 53% Non-GSR; Table 1), reducing the need for resampling or class-weight adjustments. However, the within-class heterogeneity is notable: the GSR label encompasses four distinct chemical subclasses (PbBaSb, PbBa, PbSb, BaSb), each with a different elemental profile (Figure 2, Table 3). This heterogeneity may create challenges for models that assume a single decision boundary, and suggests that per-subclass performance metrics will be important during evaluation.

Finally, the heatmap of mean elemental composition (Figure 2) confirms that the classic Pb-Ba-Sb signature is the strongest differentiator, consistent with our hypothesis that lead, barium, and antimony will emerge as the most important features in model interpretability analyses.

### 5.2 Data Cleaning and Preprocessing Plan

Based on the EDA findings, our preprocessing plan for the modeling phase includes the following steps, which represent some revisions from our original proposal:

1. **Feature selection:** We will focus modeling on the 27 informative elements identified through the sparsity analysis, rather than all 89 elemental columns. The 62 sparse elements contribute negligible signal and would add noise, particularly for linear models. This is a change from our original plan, which proposed using all elemental features.

2. **Handling ambiguous particles:** Ambiguous particles (Pb, Ba, Sb, Sr) will be excluded from the primary binary classification task, as planned. However, we will revisit them during failure analysis to examine whether trained models assign them to GSR or Non-GSR with high confidence, which could provide insight into the nature of these borderline particles.

3. **Feature engineering:** We plan to engineer elemental ratio features (e.g., Pb/Ba, Sb/Ba, Pb/Sb) as originally proposed. The EDA confirms that these elements have distinct concentration patterns across classes, and ratios may capture discriminative information that raw concentrations alone do not.

4. **Scaling:** StandardScaler will be applied for models that require it (logistic regression, neural networks). Tree-based models (XGBoost) do not require feature scaling and will receive unscaled inputs.

5. **Train-test split strategy:** Given the large dataset size (2.3 million particles for binary classification), we will use a stratified train-test split rather than k-fold cross-validation for initial model development, reserving cross-validation for final model comparison. We will also explore cross-dataset validation (train on NFI, test on NIST) as originally planned.

6. **No imputation needed:** The elemental composition data does not contain traditional missing values; zero values represent the absence of a detected element, which is a meaningful measurement. No imputation is required.

One aspect that has not changed from our original proposal is the model lineup: we still plan to train logistic regression (baseline), XGBoost (tree-based), and a fully connected neural network (deep learning on tabular data), with a CNN on spectral TIFF images as a stretch goal if time permits.

---

## Appendix A: Data Dictionary

The dataset (`particle_labeled.parquet`) contains 2,801,667 rows and 95 columns. Each row represents a single particle measured by SEM/EDS.

### Metadata Columns

| Column | Type | Description |
|---|---|---|
| `stub_id` | int | Identifier for the SEM stub (sample carrier) on which the particle was found |
| `particle_id` | int | Unique identifier for the particle within its stub |
| `relevance_class` | string | Original NFI expert-assigned particle classification (27 classes, e.g., PbSbBa, CuZn, BaCaSiS) |
| `merged_relevance_class` | string | NFI documentation-merged classification (consolidates variant spellings/orderings) |
| `final_class` | string | Fully merged particle class used in this analysis (15 classes; see mapping below) |
| `label` | string | NIST-informed label: "GSR", "Non_GSR", or "Ambiguous" |

### Elemental Composition Columns (89 columns)

Each of the following columns represents the weight-percent concentration of a chemical element detected in the particle by energy dispersive X-ray spectroscopy. Values are continuous (float64) and range from 0.0 (element not detected) upward. A value of 0.0 is not a missing value; it indicates the element was below the detection threshold for that particle.

| Column | Element | Column | Element | Column | Element |
|---|---|---|---|---|---|
| `ac` | Actinium | `hf` | Hafnium | `pm` | Promethium |
| `ag` | Silver | `hg` | Mercury | `po` | Polonium |
| `al` | Aluminum | `ho` | Holmium | `pr` | Praseodymium |
| `ar` | Argon | `i` | Iodine | `pt` | Platinum |
| `as` | Arsenic | `in` | Indium | `pu` | Plutonium |
| `at` | Astatine | `ir` | Iridium | `ra` | Radium |
| `au` | Gold | `k` | Potassium | `rb` | Rubidium |
| `b` | Boron | `kr` | Krypton | `re` | Rhenium |
| `ba` | Barium | `la` | Lanthanum | `rh` | Rhodium |
| `bi` | Bismuth | `lu` | Lutetium | `rn` | Radon |
| `br` | Bromine | `mg` | Magnesium | `ru` | Ruthenium |
| `ca` | Calcium | `mn` | Manganese | `s` | Sulfur |
| `cd` | Cadmium | `mo` | Molybdenum | `sb` | Antimony |
| `ce` | Cerium | `n` | Nitrogen | `sc` | Scandium |
| `cl` | Chlorine | `na` | Sodium | `se` | Selenium |
| `co` | Cobalt | `nb` | Niobium | `si` | Silicon |
| `cr` | Chromium | `nd` | Neodymium | `sm` | Samarium |
| `cs` | Cesium | `ne` | Neon | `sn` | Tin |
| `cu` | Copper | `ni` | Nickel | `sr` | Strontium |
| `dy` | Dysprosium | `np` | Neptunium | `ta` | Tantalum |
| `er` | Erbium | `o` | Oxygen | `tb` | Terbium |
| `eu` | Europium | `os` | Osmium | `tc` | Technetium |
| `f` | Fluorine | `p` | Phosphorus | `te` | Tellurium |
| `fe` | Iron | `pa` | Protactinium | `th` | Thorium |
| `fr` | Francium | `pb` | Lead | `ti` | Titanium |
| `ga` | Gallium | `pd` | Palladium | `tl` | Thallium |
| `gd` | Gadolinium | | | `tm` | Thulium |
| `ge` | Germanium | | | `u` | Uranium |
| | | | | `v` | Vanadium |
| | | | | `w` | Tungsten |
| | | | | `xe` | Xenon |
| | | | | `y` | Yttrium |
| | | | | `yb` | Ytterbium |
| | | | | `zn` | Zinc |
| | | | | `zr` | Zirconium |

### Final Class Mapping

| Original Relevance Classes | Final Class | Label |
|---|---|---|
| PbSbBa, PbSbBaSn, PbSbBaSr | PbBaSb | GSR |
| PbBa, PbBaSn | PbBa | GSR |
| PbSb, PbSbSn | PbSb | GSR |
| BaSb, BaSbSn | BaSb | GSR |
| BaAl, BaAlS | BaAl | Non-GSR |
| BaCaSi, BaCaSiS | BaCaSi | Non-GSR |
| CuZn | CuZn | Non-GSR |
| ZnTi | ZnTi | Non-GSR |
| Hg, SbHg | Hg | Non-GSR |
| TiZnGd | TiZnGd | Non-GSR |
| GaCuSn | GaCuSn | Non-GSR |
| Pb | Pb | Ambiguous |
| Ba, BaSi, BaSr, BaSn | Ba | Ambiguous |
| Sb, SbSn | Sb | Ambiguous |
| Sr | Sr | Ambiguous |

### Informative Elements (27 elements with >1% non-zero rate)

O, S, Cu, Ba, Al, Si, Ca, Pb, Sb, Fe, Zn, Cl, K, Na, Mg, Ti, Sn, P, Mn, As, Cr, Br, Mo, Sr, Ni, W, Hg

---

## Appendix B: Summary of Figures and Tables

| Item | Description | Location |
|---|---|---|
| Table 1 | Label distribution (GSR, Non-GSR, Ambiguous) | Section 4.1 |
| Table 2 | Informative vs. sparse element counts | Section 4.2 |
| Table 3 | Final class distribution with labels | Section 4.4 |
| Table 4 | Strongest element correlations among GSR particles | Section 4.5 |
| Table 5 | PCA variance explained | Section 4.6 |
| Figure 1 | Bar chart: proportion of particles with non-zero values per element | Section 4.2 |
| Figure 2 | Heatmap: mean elemental composition by particle class | Section 4.3 |
| Figure 3 | Stacked bar chart: particle count by class and label | Section 4.4 |
| Figure 4 | Correlogram: element correlations within GSR particles | Section 4.5 |
| Figure 5 | PCA scatter plots: GSR vs. Non-GSR and by particle class | Section 4.6 |
| Figure 6 | PCA loadings for PC1 and PC2 | Section 4.6 |
| Figure 7 | Ambiguous particles projected into PCA space | Section 4.6 |
