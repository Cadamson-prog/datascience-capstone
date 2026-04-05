# Data Dictionary for:
## EDA of the NFI Particle dataset with GSR labels

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