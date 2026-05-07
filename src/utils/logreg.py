"""
Author: Carlos Adamson
Year:   2026

Purpose:
    Functions supporting logistic regression modeling & reproducibility.
"""

import numpy as np
import pandas as pd


def engineer_features_logistic(df):
    """
    Engineer features for logistic regression model.

    Original Author: Carlos Adamson
    """

    df = df.copy()
    eps = 1e-6

    # --------------------------------------------------
    # 0. Identify core element groups used in engineering
    # --------------------------------------------------
    direct_elements = [col for col in ["pb", "ba", "sb"] if col in df.columns]
    confounder_elements = [col for col in ["zn", "cu", "ti"] if col in df.columns]

    # Numeric elemental columns that are not identifiers or labels
    non_feature_cols = {
        "stub_id",
        "particle_id",
        "relevance_class",
        "merged_relevance_class",
        "final_class",
        "label",
        "target",
    }
    element_cols = [
        col
        for col in df.select_dtypes(include=[np.number]).columns
        if col not in non_feature_cols
    ]
    # Store all new features here first
    new_features = {}

    # --------------------------------------------------
    # 1. Log transformations
    # --------------------------------------------------
    for col in ["pb", "ba", "sb", "zn", "cu", "ti"]:
        if col in df.columns:
            new_features[f"log_{col}"] = np.log1p(df[col])

    # --------------------------------------------------
    # 2. Ratios among core GSR elements
    # --------------------------------------------------
    if all(col in df.columns for col in ["pb", "ba"]):
        new_features["log_pb_ba_ratio"] = np.log1p(df["pb"] / (df["ba"] + eps))

    if all(col in df.columns for col in ["pb", "sb"]):
        new_features["log_pb_sb_ratio"] = np.log1p(df["pb"] / (df["sb"] + eps))

    if all(col in df.columns for col in ["ba", "sb"]):
        new_features["log_ba_sb_ratio"] = np.log1p(df["ba"] / (df["sb"] + eps))

    # --------------------------------------------------
    # 3. Ratios vs confounders
    # --------------------------------------------------
    if all(col in df.columns for col in ["pb", "zn"]):
        new_features["log_pb_zn_ratio"] = np.log1p(df["pb"] / (df["zn"] + eps))

    if all(col in df.columns for col in ["sb", "cu"]):
        new_features["log_sb_cu_ratio"] = np.log1p(df["sb"] / (df["cu"] + eps))

    if all(col in df.columns for col in ["ba", "ti"]):
        new_features["log_ba_ti_ratio"] = np.log1p(df["ba"] / (df["ti"] + eps))

    # -----------------------------
    # 4. Domain summary features
    # -----------------------------
    if direct_elements:
        gsr_sum = df[direct_elements].sum(axis=1)
    else:
        gsr_sum = pd.Series(0, index=df.index)

    if confounder_elements:
        conf_sum = df[confounder_elements].sum(axis=1)
    else:
        conf_sum = pd.Series(0, index=df.index)

    if element_cols:
        total_mass = df[element_cols].sum(axis=1) + eps
    else:
        total_mass = pd.Series(eps, index=df.index)

    if direct_elements and confounder_elements:
        new_features["log_gsr_over_confounders"] = np.log1p(gsr_sum / (conf_sum + eps))

    # Composition / percentage features
    for col in element_cols:
        new_features[f"{col}_pct"] = df[col] / total_mass

    # -----------------------------
    # 5. Interaction terms
    # -----------------------------
    if all(col in df.columns for col in ["pb", "sb"]):
        new_features["pb_sb_interaction"] = df["pb"] * df["sb"]

    if all(col in df.columns for col in ["ba", "sb"]):
        new_features["ba_sb_interaction"] = df["ba"] * df["sb"]

    if all(col in df.columns for col in ["pb", "ba"]):
        new_features["pb_ba_interaction"] = df["pb"] * df["ba"]

    # -----------------------------
    # 6. Diversity / complexity
    # -----------------------------
    if element_cols:
        new_features["element_diversity"] = (df[element_cols] > 0).sum(axis=1)

    # -----------------------------
    # 7. Combine all at once
    # -----------------------------
    feature_df = pd.DataFrame(new_features, index=df.index)
    df_out = pd.concat([df, feature_df], axis=1)

    return df_out
