"""
Author: Brendan OConnell
Year:   2026

Purpose: 
    For reference only. Not to be reused.
    Temp script to read, concatenate, and merge the raw data files from the NFI GitHub repository.

How it worked:
    The NFI GitHub repo was cloned locally.
    This script was created & placed in the root directory of the cloned repo.
    Steps of execution:
    - Reads in the source, stub, and stub source CSV files.
    - Reads and concatenates the particle CSV files (particle_1 through particle_14) into a single DataFrame.
    - Merges all data together based on the established relationships.
    - Saves the final DataFrame as a Parquet file for efficient storage and retrieval.

Output File:
    `data/raw/NFI/nfi_particle_data_full.parquet`
    This file was originally created using this script in the cloned NFI repo.
    It was then copied to the above path in this project repository.

Original raw CSV files can be found here:
https://github.com/NetherlandsForensicInstitute/gunshot-residue
"""

import pandas as pd

# Read in data files for Source, Stub, and Stub Source
source_df = pd.read_csv('data/source.csv')
stub_df = pd.read_csv('data/stub.csv')
stub_source_df = pd.read_csv('data/stub_source.csv')

# Build the particle DF. Read the first file with headers to establish column names
p = pd.read_csv('data/particle_1.csv')

# Read and concatenate the remaining files, which have no headers (particle_2 through particle_14)
for i in range(2, 15):
    temp = pd.read_csv(f'data/particle_{i}.csv', header=None, names=p.columns)
    p = pd.concat([p, temp], ignore_index=True)

## Table Relationships:
# stub_df.id = p.stub_id
nfi_particle_data = p.merge(stub_df, how = "left", left_on='stub_id', right_on='id', suffixes=('_particle', '_stub'))

# stub_df.id = stub_source_df.stub_id
stub_source_unique = stub_source_df.drop_duplicates(subset='stub_id', keep='first')
nfi_particle_data = nfi_particle_data.merge(stub_source_unique, how='left', on='stub_id')

# source_df.id = stub_source_df.source_id
nfi_particle_data = nfi_particle_data.merge(source_df, how='left', left_on='source_id', right_on='id', suffixes=('', '_source'))
nfi_particle_data.shape

# Save final DF as a Parquet file for efficient storage and retrieval
nfi_particle_data.to_parquet('data/nfi_particle_data_full.parquet', index=False, engine="fastparquet")
