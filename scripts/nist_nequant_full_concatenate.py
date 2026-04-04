import pandas as pd
from pathlib import Path

# nequant = "neQuant"
# nequant = "neQuantC0s JORS[GSR+Base]"
# nequant = "neQuantC3s JORS[GSR+Base]"
nequant = "neQuantC6s JORS[GSR+Base]"
raw_nist_dir = Path("data/raw/NIST")
output_path = Path(f"data/processed/nist_concatenated_parquets/nist_{nequant}_concatenated_data.parquet")


def normalize_columns(df):
    """Normalize element/uncertainty column names that include a K_FLOAT suffix.

    Examples:
        PB_K_FLOAT   -> PB
        U_PB_K_FLOAT -> U_PB_
    """
    renamed = {}
    for col in df.columns:
        if col.endswith("_K_FLOAT"):
            base = col[: -len("_K_FLOAT")]   # strip _K_FLOAT
            if base.startswith("U_"):
                base = base + "_"            # restore trailing _ for uncertainty cols
            renamed[col] = base
    return df.rename(columns=renamed)


dfs = []
for subdir in sorted(raw_nist_dir.iterdir()):
    if not subdir.is_dir():
        continue
    parquet_file = subdir / f"{nequant}.parquet"
    if not parquet_file.exists():
        print(f"Warning: {parquet_file} not found, skipping.")
        continue
    df = pd.read_parquet(parquet_file)
    df["sample_source"] = subdir.name
    df = normalize_columns(df)
    dfs.append(df)

print(f"Loaded {len(dfs)} subdirectories.")
concatenated = pd.concat(dfs, ignore_index=True)
print(f"Total rows: {len(concatenated)}")
print(f"Distinct sample_source values: {concatenated['sample_source'].nunique()}")

concatenated.to_parquet(output_path, index=False)
print(f"Written to {output_path}")
