# NFI Gunshot Residue Dataset

**Citation:** T. Matzen et al. "Objectifying evidence evaluation for gunshot residue comparisons using machine learning on criminal case data." *Forensic Science International* 335 (2022): 111293

**Description:** Dataset from the Netherlands Forensic Institute (NFI) for gunshot residue comparisons. Contains data from real criminal cases as well as samples created for research purposes.

**Source:** https://github.com/NetherlandsForensicInstitute/gunshot-residue

> Note: Visit the source GitHub repo linked above to access the raw data files.

## Steps for Raw Data File Conversion

1. Clone the NFI GitHub repository locally.
2. Copy `src/scripts/nfi_particle_data_full.py` script to the root dir of cloned NFI repo.
3. Run the python script: `python nfi_particle_data_full.py`
4. The output parquet file from that script is what is copied into this repository's `data/raw/NFI/` directory.