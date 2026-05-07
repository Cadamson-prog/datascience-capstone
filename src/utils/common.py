"""
Authors: Carlos Adamson / Brendan OConnell
Year:    2026

Purpose:
    Common utility functions to support notebook exploration & reproducibility.
"""

import numpy as np


def sentinel_divide(n, d):
    """
    Divide n by d, but return a sentinel value if 'd=0'.

    Used for feature engineering to avoid 'NaN' and 'inf' quotient when 'd=0'.
    The usage of this is discussed in detail here:
        `notebooks/02_feature_processing/engineering/feature_exploration_xgboost.ipynb`

    Args:
        n: Numerator
        d: Denominator

    Returns:
        Quotient of n/d, or a sentinel value if d=0.

    Original Author: Brendan OConnell
    """
    sentinel = -1
    safe_d = np.where(d == 0, sentinel, d)
    return n / safe_d


def safe_divide_with_eps(n, d):
    """
    Divide n by d, but use epsilon value if 'd=0'.

    Similar to 'sentinel_divide', but uses a small epsilon value instead of a sentinel.
    Used for feature engineering to avoid 'NaN' and 'inf' quotient when 'd=0'.

    Comments on epsilon vs sentinel, and potential bias, is covered in detail here:
        `notebooks/02_feature_processing/engineering/feature_exploration_xgboost.ipynb`

    Args:
        n: Numerator
        d: Denominator

    Returns:
        Quotient of n/d, or a small epsilon value if d=0.

    Original Author: Brendan OConnell
    """
    e = 1e-6
    safe_d = np.where(d == 0, e, d)
    return n / safe_d


def get_row_nearest_threshold(df, threshold):
    """
    Get the row in the DataFrame where the 'Threshold' column is closest to the specified threshold value.

    Original Author: Carlos Adamson
    """

    return df.loc[[(df["Threshold"] - threshold).abs().idxmin()]]


def get_best_f1_row(df):
    """
    Get the row in the DataFrame with the highest F1 score.

    Original Author: Carlos Adamson
    """

    return df.loc[[df["F1"].idxmax()]]


def get_high_specificity_row(df, min_recall=0.70):
    """
    Get the row in the DataFrame with the lowest FPR (highest specificity) among those with Recall >= min_recall.

    Original Author: Carlos Adamson
    """

    candidates = df[df["Recall"] >= min_recall].copy()
    if candidates.empty:
        candidates = df.copy()
    idx = candidates.sort_values(
        ["FPR", "FN", "Threshold"], ascending=[True, True, False]
    ).index[0]
    return df.loc[[idx]]


def get_high_sensitivity_row(df, min_precision=0.10):
    """
    Get the row in the DataFrame with the lowest FNR (highest sensitivity) among those with Precision >= min_precision.

    Original Author: Carlos Adamson
    """

    candidates = df[df["Precision"] >= min_precision].copy()
    if candidates.empty:
        candidates = df.copy()
    idx = candidates.sort_values(
        ["FNR", "FP", "Threshold"], ascending=[True, True, True]
    ).index[0]
    return df.loc[[idx]]


def cap_join(lst, n=10):
    """
    Join a list into a string, but cap the number of items to 'n'.

    Original Author: Brendan OConnell
    """
    return ", ".join(str(x).capitalize() for x in lst[:n])
