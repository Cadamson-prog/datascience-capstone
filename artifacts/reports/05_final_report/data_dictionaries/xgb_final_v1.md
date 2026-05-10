# XGBoost Final Model v1

## Data Dictionary

The final NFI dataset used for the XGBoost model contains 2,294,985 rows and 101 columns. Each row represents a single particle measured by SEM/EDS. This dataset has 89 elemental features and 7 engineered features for a total of 96 feature columns.

### Metadata Columns

> **Composite Key:** `stub_id` and `particle_id` together uniquely identify each row. Neither column is unique on its own — the pairing is always unique across the full dataset.

| Column | Type | Description |
|---|---|---|
| `stub_id` | int | Identifier for the SEM stub (sample carrier) on which the particle was found. Forms composite key with `particle_id`. |
| `particle_id` | int | Identifier for the particle within its stub. Forms composite key with `stub_id`. |
| `final_class` | string | Fully merged particle class used in this analysis (see `eda_nfi_particle_labeled.md` for class mapping) |
| `label` | string | NIST-informed label: "GSR" or "Non_GSR" (ambiguous particles excluded from this dataset) |
| `target` | int | Binary classification target derived from `label`: 1 = GSR, 0 = Non_GSR |

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

Seven features engineered from elemental composition to improve GSR discrimination.

| Column | Datatype | PR-AUC Estimate | Description |
|---|---|---|---|
| `pb_sb_over_non_ba_mass` | float | 0.9979 | (Pb + Sb) as a fraction of total elemental mass excluding barium. Isolates the Pb & Sb pair to distinguish GSR from barium-heavy Non-GSR confounders (BaAl, BaCaSi). |
| `pb_ba_over_non_sb_mass` | float | 0.6925 | (Pb + Ba) as a fraction of total elemental mass excluding antimony. Measures the Pb & Ba pair's dominance over overall particle composition. |
| `ba_sb_over_non_pb_mass` | float | 0.6172 | (Ba + Sb) as a fraction of total elemental mass excluding lead. Captures the Ba & Sb pair signal for BaSb-type GSR particles. |
| `gsr_over_confounders` | float | 0.9430 | (Pb + Sb) / (Ca + Si + Al + Fe + Ti + Zn + Cu). Ratio of GSR signal to common environmental and mineral confounders, excluding barium due to its overlap in both GSR and Non-GSR classes. Uses a sentinel value of −1 when the denominator = 0, allowing XGBoost to distinguish undefined ratios from reliable positive ones. |
| `pb_times_sb` | float | 0.8323 | Multiplicative product of Pb × Sb. Penalizes trace amounts of both elements, addressing false-positive edge cases where barium-heavy Non-GSR particles have only trace Pb and Sb contamination. |
| `cu_zn_over_mass` | float | 0.4329 | (Cu + Zn) as a fraction of total elemental mass. Targets brass (CuZn) Non-GSR particles that contain trace Pb and Sb. |
| `ti_zn_over_mass` | float | 0.4010 | (Ti + Zn) as a fraction of total elemental mass. Targets TiZnGd and ZnTi Non-GSR glass particles that have elevated core GSR element counts. |
