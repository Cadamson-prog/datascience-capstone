"""
Author: Kristin Predeck
Year:   2026

Purpose:
    Functions supporting neural network modeling & reproducibility.
"""

import numpy as np


def multiplicative_replacement(X, delta=None):
    """
    For each zero entry, replace with delta (default: half the minimum non-zero
    value in that column). Non-zero entries are scaled down proportionally so
    rows still sum to the same total.

    Original Author: Kristin Predeck
    """

    X = X.copy().astype(float)

    if delta is None:
        nonzero_vals = X[X > 0]
        delta = nonzero_vals.min() / 2 if len(nonzero_vals) > 0 else 1e-10

    row_sums = X.sum(axis=1, keepdims=True)

    for i in range(X.shape[0]):
        zero_mask = X[i] == 0
        n_zeros = zero_mask.sum()
        if n_zeros > 0 and row_sums[i, 0] > 0:
            X[i, zero_mask] = delta
            correction = 1 - (n_zeros * delta / row_sums[i, 0])
            X[i, ~zero_mask] *= correction

    return X


def clr_transform(X):
    """
    Centered Log-Ratio transform.

    Original Author: Kristin Predeck
    """

    log_X = np.log(X)
    geometric_mean = log_X.mean(axis=1, keepdims=True)
    return log_X - geometric_mean


def engineer_nn_features(df, element_cols):
    """
    Engineer features for neural network model.

    Original Author: Kristin Predeck
    """

    X_raw = df[element_cols].values
    X_replaced = multiplicative_replacement(X_raw)
    X_clr = clr_transform(X_replaced).astype(np.float32)
    X_presence = (X_raw > 0).astype(np.float32)

    total_mass = df[element_cols].sum(axis=1).values
    denom = total_mass - df["ba"].values - df["o"].values
    safe_denom = np.where(denom == 0, -1, denom)
    pb_sb_ratio = ((df["pb"].values + df["sb"].values) / safe_denom).astype(np.float32)
    log_pb_sb = np.log1p(df["pb"].values + df["sb"].values).astype(np.float32)

    X_features = np.hstack(
        [X_clr, X_presence, pb_sb_ratio.reshape(-1, 1), log_pb_sb.reshape(-1, 1)]
    )
    return X_features


def build_feature_matrix(condition_cfg, df_nn, df_raw, indices):
    """
    Extract feature matrix for condition.

    Original Author: Kristin Predeck
    """

    source = condition_cfg["source"]
    cols = condition_cfg["cols"]

    if source == "nn":
        X = df_nn[cols].values[indices].astype(np.float32)
    else:
        X = df_raw[cols].values[indices].astype(np.float32)

    extra = condition_cfg.get("extra_from_nn", [])
    if extra:
        X_extra = df_nn[extra].values[indices].astype(np.float32)
        X = np.hstack([X, X_extra])

    return X
