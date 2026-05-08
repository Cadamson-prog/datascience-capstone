"""Unit tests for src/utils/xgb.py"""

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import average_precision_score

from src.utils import xgb


class TestComputePrauc:
    """`compute_prauc` returns the PR-AUC of `vals` against the binary
    `target` column (1 = positive), rounded to 4 decimal places."""

    def test_perfect_ordering_returns_one(self):
        df = pd.DataFrame({"target": [1, 1, 0, 0]})
        vals = [0.9, 0.8, 0.2, 0.1]
        assert xgb.compute_prauc(df, vals) == 1.0

    def test_matches_sklearn_average_precision(self):
        # Use a non-trivial dataset where AP < 1
        df = pd.DataFrame({"target": [1, 0, 1, 0, 1, 0]})
        vals = np.array([0.9, 0.8, 0.7, 0.4, 0.3, 0.1])
        y = (df["target"] == 1).astype(int).values
        expected = round(average_precision_score(y, vals), 4)
        assert xgb.compute_prauc(df, vals) == expected

    def test_result_rounded_to_four_decimal_places(self):
        df = pd.DataFrame({"target": [1, 0, 1, 0, 1, 0]})
        vals = [0.55, 0.45, 0.35, 0.25, 0.15, 0.05]
        result = xgb.compute_prauc(df, vals)
        # `round(x, 4)` is bit-exact, so rounding the result again leaves it
        # unchanged.
        assert result == round(result, 4)

    def test_target_values_other_than_one_treated_as_negative(self):
        # The function builds y as `(target == 1).astype(int)`, so any value
        # that isn't exactly 1 (including 0, 2, NaN-via-coerce-fail) is a
        # negative. Here we mix 0 and 2 - both should be negatives.
        df = pd.DataFrame({"target": [1, 0, 2, 1]})
        vals = [0.9, 0.1, 0.2, 0.8]
        y = np.array([1, 0, 0, 1])
        expected = round(average_precision_score(y, vals), 4)
        assert xgb.compute_prauc(df, vals) == expected

    def test_returns_float(self):
        df = pd.DataFrame({"target": [1, 0]})
        result = xgb.compute_prauc(df, [0.9, 0.1])
        assert isinstance(result, float)

    def test_does_not_mutate_input_dataframe(self):
        df = pd.DataFrame({"target": [1, 0, 1, 0], "extra": [10, 20, 30, 40]})
        snapshot = df.copy(deep=True)
        xgb.compute_prauc(df, [0.9, 0.1, 0.8, 0.2])
        pd.testing.assert_frame_equal(df, snapshot)
