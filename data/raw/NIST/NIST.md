# NIST Public Data Repository: Automated Particle Analysis (SEM/EDS)

## Data from samples known to have been exposed to gunshot residue and from samples occasionally mistaken for gunshot residue - like brake dust and fireworks.

**Citation:** Ritchie, Nicholas W. M., Renolds, Amy  (2021), Automated particle analysis (SEM/EDS) data from samples known to have been exposed to gunshot residue and from samples occasionally mistaken for gunshot residue - like brake dust and fireworks., National Institute of Standards and Technology, https://doi.org/10.18434/mds2-2476 (Version: 1.0, Accessed 2026-04-02)

**Description:** The dataset consists of analyses of 30 discrete samples: 12 from sampling automobiles ("brake dust"), 10 from sampling fireworks ("sparklers" and "spinners" and "roman candles"), 8 from shooter's left or right hands. The raw data from each analysis is in the file pair "data.pxz" and "data.hdz". PXZ + HDZ file pairing is known as a Zeppelin. 

**Source:** https://data.nist.gov/od/id/mds2-2476

> Note: You can visit the source linked above to access the original data files, but they are formatted as Zeppelins (HDZ/PXZ pairs) for Julia.  They have been converted to Parquet and can be accessed in this repository for convenience.

## Steps for Raw Data File Conversion

The difficulty here is that the raw data files are stored as PXZ & HDZ files, a pairing known as a Zeppelin. The steps below were used to convert the Zeppelin format to Parquet. The conversion required the installation of the Julia Programming Language (https://julialang.org/).

1) Download all 30 zips (1 for each discrete sample).
2) For each sample, unzip the contents into a local directory.
3) Install Julia & open Julia REPL
4) Follow the `julia.jl` script to process each Zeppelin conversion (see `scripts/julia/julia.jl`)
    - OR run each source/target individually with `scripts/julia/hdz_to_parquet.jl` from command prompt (see usage)
    - OR run full batch with `scripts/julia/batch_hdz_to_parquet.jl` from command prompt (see usage -- change job paths accordingly)

## Additional Notes for each NIST sample subdirectory

- The configuration.txt file details the configuration of the testing and data collection for the sample.
- 