# NFI Gunshot Residue Dataset

**Citation:** T. Matzen et al. "Objectifying evidence evaluation for gunshot residue comparisons using machine learning on criminal case data." *Forensic Science International* 335 (2022): 111293

**Description:** Dataset from the Netherlands Forensic Institute (NFI) for gunshot residue comparisons. Contains data from real criminal cases as well as samples created for research purposes.

**Source:** https://github.com/NetherlandsForensicInstitute/gunshot-residue

> Note: Visit the source GitHub repo linked above to access the raw data files.

## Steps for Raw Data File Conversion

1. Clone the NFI GitHub repository locally.
2. Create a python script that:
    - Reads in each CSV file
    - Concatenates the Particle files together into a single table
    - Joins all tables together into a single table, using Particle ID as the Primary Key.
    - Writes the final raw table to a compressed Parquet format.
3. Run the python script (see `scripts/nfi_particle_data_full.py`)
4. Copy the script & Parquet output file to our project repository.