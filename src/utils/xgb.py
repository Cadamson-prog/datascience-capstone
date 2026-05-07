"""
Author: Brendan OConnell
Year:   2026

Purpose:
    Functions supporting XGBoost modeling & reproducibility.
"""

# Using "average precision score" to estimate PR-AUC for standalone feature precision
from sklearn.metrics import average_precision_score as ap_score


def compute_prauc(df, vals):
    """
    Compute PR-AUC for the predicted vals against the true target labels in the DataFrame.

    Args:
        df (DataFrame): The DataFrame containing the true target labels.
        vals (array-like): The predicted values for which to compute PR-AUC.

    Returns:
        float: The computed PR-AUC score, rounded to 4 decimal places.

    Original Author: Brendan OConnell
    """

    y = (df["target"] == 1).astype(int).values  # GSR
    return round(ap_score(y, vals), 4)
