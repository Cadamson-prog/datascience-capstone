"""
This script was used to read, concatenate, and merge the raw data files from the NFI GitHub repository. 
The final output is a single Parquet file containing the full particle data, 
with additional information from the source and stub raw files.

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
