"""
Authors: Kristin Predeck / Brendan OConnell
Year:    2026

Purpose:
    Functions supporting NIST data processing & reproducibility.
"""

import re


def extract_class(s):
    """
    Extract the bracketed class name from a NIST classification string.

    Original Author: Kristin Predeck
    """

    match = re.search(r"\[(.+?):", str(s))
    if match:
        return match.group(1)
    return "Unknown"


def label_gsr(class_name):
    """Label a NIST class string as GSR, Non_GSR, or Low_Quality.

    Original Author: Kristin Predeck
    """

    class_lower = class_name.lower()
    if "classic gsr" in class_lower or "gsr" in class_lower:
        return "GSR"
    elif class_lower in ["#unclassified#", "lowcounts", "low counts"]:
        return "Low_Quality"
    else:
        return "Non_GSR"


def renormalize_with_oxygen(df_copy, non_o_element_cols, oxygen_col="o"):
    """
    Renormalize NIST elemental percentages to include oxygen for cross-testing the NFI-trained models.

    Oxygen is present in the samples but not included in the original NIST element weight percentages.
    However, the NFI dataset includes oxygen in the elemental percentages.
    This function scales the non-oxygen element percentages so that they sum to 100% when oxygen is included.

    Args:
        df_copy (DataFrame): A copy of the NIST DataFrame to be renormalized.
        non_o_element_cols (list): List of column names for the non-oxygen elements to be scaled.
        oxygen_col (str): The column name for the oxygen element percentage (default is 'o').

    Returns:
        DataFrame: DF with the non-oxygen element percentages scaled to include oxygen.

    Original Author: Brendan OConnell
    """

    df_ret = df_copy
    scale = (100 - df_ret[oxygen_col]) / 100.0
    df_ret[non_o_element_cols] = df_ret[non_o_element_cols].multiply(scale, axis=0)
    return df_ret
