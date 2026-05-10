**Author:**  Brendan OConnell
**Date:** April 2026

### Informal observations of the NIST dataset

Our primary focus will be on the NFI dataset, but we may end up using the NIST dataset for model testing. After some initial EDA on the NIST dataset, there are some noteworthy observations that may need revisiting if we decide to use it for model testing.
For starters, all 30 sources have configuration files that have been reviewed. The data collection and general configuration for all 30 samples has been confirmed to be the same. However, aside from the obvious “GSR” vs. “Non-GSR” descriptors, there are some differences in the reprocessing of data which could have implications in terms of model accuracy. There are also some differences in the structure of the data as well as the scaling techniques and potentially quantification methods as compared to the NFI dataset. These differences will be detailed below.
The main files retrieved from the NIST source are stored as a pair of files known as a Zeppelin, which consists of an HDZ header file and PXZ data file. The steps for processing these files are outlined here: https://github.com/bkoconnell/datascience-capstone/blob/main/data/raw/NIST/NIST.md
Steps include downloading the Julia programming software, installing specific dependencies, and running some commands that can be found in our scripts directory in the GitHub repository. A batch script was also created to process all raw data files into parquet files for EDA. These parquet files can be found in the data/raw/ directory of our GitHub repository.
The original data from the particle scan is in the data zeppelin, which was processed in real-time using a “QuickQuant” method of quantification, but it only processed the data against 17 reference standard spectra which did not include Pb (lead) or Sb (antimony). The converted “data.parquet” files have been reviewed to verify this. Since 2 out of the 3 core GSR elements are not included in the original data files, these will not be of much use for our research. To be clear, Pb and Sb are not missing in the sense that they weren’t in the particle, they’re only missing from the original data processing because the configuration file specifically did not tell the software to look for them (they were not part of the original 17 elements listed in the config file):
 

After the initial processing, the operator reprocessed the TIFF/MSA data against the 25 keV spectra, which does include Pb and Sb.  In total, the reprocessed files include 32 total elements (15 more than the original processing). All 32 of these elements exist in the NFI dataset. The most important thing to recognize about the reprocessed data is that there are different quantification methods used and different classification rules used. The following statements are true for all 30 samples:
●	All have data Zeppelins that we cannot use because they did not process any values for Pb or Sb
●	All have reprocessed the original data against the expanded 25 keV spectra which includes Pb and Sb
●	All have used the NeXLParticle vector file which details the quantification method for reprocessing the original data. The reprocessed data is stored in the neQuant Zeppelin, which is capped at 5,000 particle observations and does not include any GSR class labels
●	All have the same C-variant reprocessed neQuant files:
○	neQuantC0 (generic class labels)
○	neQuantC0s (JORS[GSR+Base] class labels)
○	neQuantC3 (generic class labels)
○	neQuantC3s (JORS[GSR+Base] class labels)
○	neQuantC6s (generic class labels)
○	neQuantC6s (JORS[GSR+Base] class labels)
●	C-variant neQuant files contain all 16k+ particle observations (not capped at 5k)
●	The NeXL open-source library suite (used for neQuant reprocessing) uses standards-based k-ratio quantification and iterative XPP matrix correction
●	All neQuant and C-variants include “uncertainty” estimates (element columns prefixed with U_), representing how confident the quantification is for that element in that particle. It is the one-sigma uncertainty estimate in the same unit as the element (weight percentage)
The shooter sources additionally have some Zeppelin files that used MLLSQ / MLLSQU (multiple linear least squares) quantification methods.
There is a “RELOCATED” folder which contains particle data identified as GSR.
Important note regarding Oxygen:
The NFI dataset includes oxygen in the sum of its elemental weights, so all 89 elements in the NFI particle data will sum to 100%.  In contract, NIST does not include oxygen in its scale. All elements for a particle except for oxygen will add up to 100, then oxygen is added on top of that. The author (Ritchie) may have alluded to this as “oxygen-by-stoichiometry” in an article where he wrote:
“ If it is not possible or not desirable to measure an element, this element can often be modeled using an unmeasured element rule. An example of one such rule is the oxygen-by-stoichiometry model.”
This may warrant further investigation. It seems that instead of measuring oxygen, like the other elements were measured, the oxygen value is obtained via calculation based on some assumptions of the other elements. It is unknown whether the difference in oxygen quantification methods between the NFI dataset and the NIST dataset has any impact on a model’s ability to classify GSR. It is suspected that some models may be more sensitive to this, while others may be able to ignore it.
Lastly, in terms of the full dataset, the GitHub repository for our project now contains the converted Zeppelin files in Parquet format in the data/raw/NIST/ folder for the corresponding sample source. At the very least, each of the 30 sample sources has parquet files for each of the neQuant reprocessed datasets and all of the neQuant C-variants. For convenience, and possibly future EDA, all neQuant variants also have Parquet formatted files that are fully concatenated across all 30 sample sources. These are located in the data/processed/nist_concatenated_parquets/ folder. Be aware that the concatenated files currently have 2 calculated fields added to them which were used to confirm the notes made regarding oxygen quantities. These 2 new fields are elemental sums with oxygen, and element sums without oxygen. It may be necessary to remove these columns if further EDA or any model testing are to be performed.
