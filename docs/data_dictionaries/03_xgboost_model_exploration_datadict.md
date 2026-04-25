# XGBoost Baseline Models

## Data Dictionary

The dataset (`engineered_features_xgboost.parquet`) contains 2,294,985 rows and 46 columns. Each row represents a single particle measured by SEM/EDS. This dataset extends the preprocessed NFI particle data with 27 informative elemental features and 14 engineered features, used across three XGBoost baseline models.

### Metadata Columns

> **Composite Key:** `stub_id` and `particle_id` together uniquely identify each row. Neither column is unique on its own — the pairing is always unique across the full dataset.

| Column | Type | Description |
|---|---|---|
| `stub_id` | int | Identifier for the SEM stub (sample carrier) on which the particle was found. Forms composite key with `particle_id`. |
| `particle_id` | int | Identifier for the particle within its stub. Forms composite key with `stub_id`. |
| `final_class` | string | Fully merged particle class used in this analysis (see `eda_nfi_particle_labeled.md` for class mapping) |
| `label` | string | NIST-informed label: "GSR" or "Non_GSR" (ambiguous particles excluded from this dataset) |
| `target` | int | Binary classification target derived from `label`: 1 = GSR, 0 = Non_GSR |

### Elemental Composition Columns (27 columns)

Each of the following columns represents the weight-percent concentration of a chemical element detected in the particle by energy dispersive X-ray spectroscopy. Values are continuous (float64) and range from 0.0 (element not detected) upward. A value of 0.0 is not a missing value; it indicates the element was below the detection threshold for that particle.

| Column | Element | Column | Element | Column | Element |
|---|---|---|---|---|---|
| `al` | Aluminum | `hg` | Mercury | `pb` | Lead |
| `as` | Arsenic | `k` | Potassium | `s` | Sulfur |
| `ba` | Barium | `mg` | Magnesium | `sb` | Antimony |
| `br` | Bromine | `mn` | Manganese | `si` | Silicon |
| `ca` | Calcium | `mo` | Molybdenum | `sn` | Tin |
| `cl` | Chlorine | `na` | Sodium | `sr` | Strontium |
| `cr` | Chromium | `ni` | Nickel | `ti` | Titanium |
| `cu` | Copper | `o` | Oxygen | `w` | Tungsten |
| `fe` | Iron | `p` | Phosphorus | `zn` | Zinc |

### Particle Classes with Labels

| Final Class | Label |
|---|---|
| PbBaSb | GSR |
| PbBa | GSR |
| PbSb | GSR |
| BaSb | GSR |
| BaAl | Non-GSR |
| BaCaSi | Non-GSR |
| CuZn | Non-GSR |
| ZnTi | Non-GSR |
| Hg | Non-GSR |
| TiZnGd | Non-GSR |
| GaCuSn | Non-GSR |

### Engineered Feature Columns

Fourteen features engineered from elemental composition to improve GSR discrimination. The "Baseline" columns indicate whether the feature was included in each model's training set (✓ = included).

| Column | Datatype | Baseline v1 | Baseline v2 | Baseline v3 | PR-AUC Estimate | Description |
|---|---|---|---|---|---|---|
| `core_gsr_count` | int | ✓ | | | 0.9976 | Count of core GSR elements present in the particle (Pb, Ba, Sb), ranging 0–3. Dropped in v2+ due to circular encoding — the feature directly replicates the expert labeling rule, causing near-immediate model convergence and suspected target leakage. |
| `log_pb_plus_sb` | float | ✓ | ✓ | | 0.9973 | log(1 + (Pb + Sb)). Additive log-compressed quantification of the core GSR element pairing of lead and antimony. Dropped in v3 to assess potential redundancy or leakage. |
| `pb_sb_over_non_ba_mass` | float | ✓ | ✓ | | 0.9979 | (Pb + Sb) as a fraction of total elemental mass excluding barium. Isolates the Pb & Sb pair to distinguish GSR from barium-heavy Non-GSR confounders (BaAl, BaCaSi). |
| `pb_sb_over_non_ba_o_mass` | float | ✓ | ✓ | | 0.9988 | (Pb + Sb) as a fraction of total elemental mass excluding barium and oxygen. Highest single-feature PR-AUC; dropped in v3 alongside `pb_sb_over_non_ba_mass` due to assess potential redundancy or leakage. |
| `pb_ba_over_non_sb_mass` | float | ✓ | ✓ | ✓ | 0.6925 | (Pb + Ba) as a fraction of total elemental mass excluding antimony. Measures the Pb & Ba pair's dominance over overall particle composition. |
| `pb_ba_over_non_sb_o_mass` | float | ✓ | ✓ | ✓ | 0.7736 | (Pb + Ba) as a fraction of total elemental mass excluding antimony and oxygen. Oxygen-excluded variant of `pb_ba_over_non_sb_mass` to assess whether oxygen dilutes signal. |
| `ba_sb_over_non_pb_mass` | float | ✓ | ✓ | ✓ | 0.6172 | (Ba + Sb) as a fraction of total elemental mass excluding lead. Captures the Ba & Sb pair signal for BaSb-type GSR particles. |
| `ba_sb_over_non_pb_o_mass` | float | ✓ | ✓ | ✓ | 0.6914 | (Ba + Sb) as a fraction of total elemental mass excluding lead and oxygen. Oxygen-excluded variant of `ba_sb_over_non_pb_mass` to assess whether oxygen dilutes signal. |
| `gsr_over_confounders` | float | ✓ | ✓ | ✓ | 0.9430 | (Pb + Sb) / (Ca + Si + Al + Fe + Ti + Zn + Cu). Ratio of GSR signal to common environmental and mineral confounders, excluding barium due to its overlap in both GSR and Non-GSR classes. Uses a sentinel value of −1 when the denominator = 0, allowing XGBoost to distinguish undefined ratios from reliable positive ones. |
| `pb_times_sb` | float | ✓ | ✓ | ✓ | 0.8323 | Multiplicative product of Pb × Sb. Penalizes trace amounts of both elements, addressing false-positive edge cases where barium-heavy Non-GSR particles have only trace Pb and Sb contamination. |
| `cu_zn_over_mass` | float | ✓ | ✓ | ✓ | 0.4329 | (Cu + Zn) as a fraction of total elemental mass. Targets brass (CuZn) Non-GSR particles that contain trace Pb and Sb. |
| `cu_zn_over_non_o_mass` | float | ✓ | ✓ | ✓ | 0.4298 | (Cu + Zn) as a fraction of total elemental mass excluding oxygen. Oxygen-excluded variant of `cu_zn_over_mass` to assess whether oxygen dilutes signal. |
| `ti_zn_over_mass` | float | ✓ | ✓ | ✓ | 0.4010 | (Ti + Zn) as a fraction of total elemental mass. Targets TiZnGd and ZnTi Non-GSR glass particles that have elevated core GSR element counts. |
| `ti_zn_over_non_o_mass` | float | ✓ | ✓ | ✓ | 0.4004 | (Ti + Zn) as a fraction of total elemental mass excluding oxygen. Oxygen-excluded variant of `ti_zn_over_mass` to assess whether oxygen dilutes signal. |
