"""
Author: Brendan OConnell
Year:   2026

Purpose:
    For reproducibility, this module contains reusable functions to support critical EDA steps.
"""

from typing import Dict
import pandas as pd
from .utils import fileops


def get_nfi_final_class_map() -> Dict[str, str]:
    """Get the NFI particle class mappings for the `relevance_class` to the `final_class`"""

    return {
        "PbSbBa": "PbBaSb",
        "PbSbBaSn": "PbBaSb",
        "PbSbBaSr": "PbBaSb",
        "PbBa": "PbBa",
        "PbBaSn": "PbBa",
        "PbSb": "PbSb",
        "PbSbSn": "PbSb",
        "BaSb": "BaSb",
        "BaSbSn": "BaSb",
        "Sb": "Sb",
        "SbSn": "Sb",
        "Ba": "Ba",
        "BaSi": "Ba",
        "BaSr": "Ba",
        "BaSn": "Ba",
        "BaAl": "BaAl",
        "BaAlS": "BaAl",
        "BaCaSi": "BaCaSi",
        "BaCaSiS": "BaCaSi",
        "CuZn": "CuZn",
        "Pb": "Pb",
        "ZnTi": "ZnTi",
        "Sr": "Sr",
        "Hg": "Hg",
        "SbHg": "Hg",
        "TiZnGd": "TiZnGd",
        "GaCuSn": "GaCuSn",
    }


def get_nfi_label_map() -> Dict[str, str]:
    """Get the NFI particle class mapping of labels for GSR/Non-GSR/Ambiguous"""

    return {
        # CONFIRMED GSR by NIST (found on known shooter samples)
        "PbBaSb": "GSR",  # NIST: Classic GSR, GSR.0, GSR.1, GSR.2
        "PbBa": "GSR",  # NIST: GSR.Pb-Ba
        "PbSb": "GSR",  # NIST: GSR.Pb-Sb
        "BaSb": "GSR",  # NIST: GSR.Ba-Sb
        # CONFIRMED NON-GSR by NIST (environmental/occupational)
        "BaAl": "Non_GSR",  # No NIST GSR equivalent
        "BaCaSi": "Non_GSR",  # No NIST GSR equivalent
        "CuZn": "Non_GSR",  # NIST: Brass — found on shooters but NOT classified as GSR
        "ZnTi": "Non_GSR",  # Environmental
        "Hg": "Non_GSR",  # Environmental
        "TiZnGd": "Non_GSR",  # Environmental
        "GaCuSn": "Non_GSR",  # Environmental
        # AMBIGUOUS if single-element particles
        "Pb": "Ambiguous",  # NIST: Lead class exists separate from GSR
        "Ba": "Ambiguous",  # NIST: Barite (BaSO4) is environmental
        "Sb": "Ambiguous",  # Could be GSR fragment or industrial
        "Sr": "Ambiguous",  # NIST: GSR.Sr-bearing exists but also Celestine mineral
    }


def create_main_data() -> pd.DataFrame:
    """
    Load and process the raw NFI particle data.

    Returns:
        DataFrame: Processed NFI particle data with final_class and label columns,
        duplicate (stub_id, particle_id) rows removed, and some metadata columns dropped.
    """

    raw_df = fileops.load_data_file("data/raw/NFI/nfi_particle_data_full.parquet")

    raw_df["final_class"] = raw_df["relevance_class"].map(get_nfi_final_class_map())
    raw_df["label"] = raw_df["final_class"].map(get_nfi_label_map())

    drop_cols = [
        "id_x",
        "sample_name",
        "project",
        "type_project",
        "ammo_type",
        "sample_type",
        "sample_source",
        "id_y",
        "source_id",
        "id",
        "name",
        "cluster",
        "group_by",
    ]
    raw_df = raw_df.drop(columns=[c for c in drop_cols if c in raw_df.columns])

    raw_df = raw_df.drop_duplicates(subset=["stub_id", "particle_id"])

    return raw_df
