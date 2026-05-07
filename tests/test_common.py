"""Unit tests for src/utils/common.py"""

import numpy as np
import pandas as pd
import pytest

from src.utils import common


# ---------------------------------------------------------------------------
# sentinel_divide
# ---------------------------------------------------------------------------
class TestSentinelDivide:
    """`sentinel_divide` returns n/d, substituting -1 for any zero in d."""

    def test_scalar_no_zero(self):
        assert common.sentinel_divide(np.array([10.0]), np.array([2.0])) == pytest.approx(5.0)

    def test_array_without_zeros(self):
        n = np.array([10.0, 6.0, 8.0])
        d = np.array([2.0, 3.0, 4.0])
        np.testing.assert_allclose(common.sentinel_divide(n, d), [5.0, 2.0, 2.0])

    def test_zero_in_denominator_uses_sentinel(self):
        # n=4, d=0 → safe_d=-1, result = 4 / -1 = -4
        n = np.array([4.0])
        d = np.array([0.0])
        np.testing.assert_allclose(common.sentinel_divide(n, d), [-4.0])

    def test_mixed_zeros_and_nonzeros(self):
        n = np.array([10.0, 5.0, 8.0])
        d = np.array([2.0, 0.0, 4.0])
        # middle entry: 5/-1 = -5
        np.testing.assert_allclose(common.sentinel_divide(n, d), [5.0, -5.0, 2.0])

    def test_no_inf_or_nan_when_d_has_zeros(self):
        n = np.array([1.0, 2.0, 3.0])
        d = np.array([0.0, 0.0, 0.0])
        out = common.sentinel_divide(n, d)
        assert np.all(np.isfinite(out))


# ---------------------------------------------------------------------------
# safe_divide_with_eps
# ---------------------------------------------------------------------------
class TestSafeDivideWithEps:
    """`safe_divide_with_eps` returns n/d, substituting 1e-6 for any zero in d."""

    def test_array_without_zeros_matches_plain_division(self):
        n = np.array([10.0, 6.0])
        d = np.array([2.0, 3.0])
        np.testing.assert_allclose(common.safe_divide_with_eps(n, d), n / d)

    def test_zero_in_denominator_uses_epsilon(self):
        n = np.array([4.0])
        d = np.array([0.0])
        np.testing.assert_allclose(common.safe_divide_with_eps(n, d), [4.0 / 1e-6])

    def test_no_inf_or_nan_when_d_has_zeros(self):
        n = np.array([1.0, 2.0])
        d = np.array([0.0, 0.0])
        out = common.safe_divide_with_eps(n, d)
        assert np.all(np.isfinite(out))

    def test_result_is_large_but_finite_for_zero_denominator(self):
        n = np.array([1.0])
        d = np.array([0.0])
        out = common.safe_divide_with_eps(n, d)
        assert out[0] == pytest.approx(1e6)


# ---------------------------------------------------------------------------
# cap_join
# ---------------------------------------------------------------------------
class TestCapJoin:
    """`cap_join` joins up to n list items, capitalizing each."""

    def test_default_cap_keeps_first_ten(self):
        lst = [f"item{i}" for i in range(15)]
        out = common.cap_join(lst)
        assert out.split(", ") == [f"Item{i}" for i in range(10)]

    def test_custom_cap(self):
        out = common.cap_join(["alpha", "beta", "gamma"], n=2)
        assert out == "Alpha, Beta"

    def test_cap_larger_than_list_returns_all(self):
        out = common.cap_join(["a", "b"], n=10)
        assert out == "A, B"

    def test_empty_list_returns_empty_string(self):
        assert common.cap_join([]) == ""

    def test_cap_zero_returns_empty_string(self):
        assert common.cap_join(["a", "b"], n=0) == ""

    def test_non_string_items_are_stringified_and_capitalized(self):
        out = common.cap_join([1, 2.5, "ok"], n=3)
        # str(1).capitalize() == "1"; str(2.5).capitalize() == "2.5"
        assert out == "1, 2.5, Ok"


# ---------------------------------------------------------------------------
# Threshold-table helpers
#
# All four operate on a DataFrame shaped like the threshold sweep tables
# produced in the evaluation notebooks. The fixture below provides one.
# ---------------------------------------------------------------------------
@pytest.fixture
def threshold_df():
    return pd.DataFrame(
        {
            "Threshold": [0.10, 0.30, 0.50, 0.70, 0.90],
            "Precision": [0.20, 0.50, 0.80, 0.90, 0.95],
            "Recall":    [0.99, 0.85, 0.75, 0.60, 0.30],
            "F1":        [0.33, 0.63, 0.77, 0.72, 0.45],
            "FPR":       [0.40, 0.20, 0.10, 0.05, 0.01],
            "FNR":       [0.01, 0.15, 0.25, 0.40, 0.70],
            "FP":        [400, 200, 100,  50,  10],
            "FN":        [ 10, 150, 250, 400, 700],
        }
    )


class TestGetRowNearestThreshold:

    def test_exact_match(self, threshold_df):
        row = common.get_row_nearest_threshold(threshold_df, 0.50)
        assert row["Threshold"].iloc[0] == 0.50

    def test_picks_closest_when_no_exact_match(self, threshold_df):
        # 0.49 is closest to 0.50
        row = common.get_row_nearest_threshold(threshold_df, 0.49)
        assert row["Threshold"].iloc[0] == 0.50

    def test_returns_single_row_dataframe(self, threshold_df):
        row = common.get_row_nearest_threshold(threshold_df, 0.50)
        assert isinstance(row, pd.DataFrame)
        assert len(row) == 1


class TestGetBestF1Row:

    def test_picks_max_f1(self, threshold_df):
        row = common.get_best_f1_row(threshold_df)
        # Best F1 in fixture is 0.77 at threshold 0.50
        assert row["F1"].iloc[0] == 0.77
        assert row["Threshold"].iloc[0] == 0.50

    def test_returns_single_row_dataframe(self, threshold_df):
        assert len(common.get_best_f1_row(threshold_df)) == 1


class TestGetHighSpecificityRow:
    """Picks lowest-FPR row whose Recall >= min_recall."""

    def test_filters_to_min_recall_then_picks_lowest_fpr(self, threshold_df):
        # Recall >= 0.70 → rows at thresholds 0.10, 0.30, 0.50.
        # Lowest FPR among them is 0.10 at threshold 0.50.
        row = common.get_high_specificity_row(threshold_df, min_recall=0.70)
        assert row["Threshold"].iloc[0] == 0.50
        assert row["FPR"].iloc[0] == 0.10

    def test_min_recall_zero_picks_lowest_fpr_overall(self, threshold_df):
        # All rows pass min_recall=0; lowest FPR is 0.01 at threshold 0.90.
        row = common.get_high_specificity_row(threshold_df, min_recall=0.0)
        assert row["Threshold"].iloc[0] == 0.90

    def test_falls_back_when_no_candidates_meet_recall(self, threshold_df):
        # No row has Recall >= 1.5 → fallback uses the full df.
        # Lowest FPR overall is at threshold 0.90.
        row = common.get_high_specificity_row(threshold_df, min_recall=1.5)
        assert row["Threshold"].iloc[0] == 0.90


class TestGetHighSensitivityRow:
    """Picks lowest-FNR row whose Precision >= min_precision."""

    def test_filters_to_min_precision_then_picks_lowest_fnr(self, threshold_df):
        # Precision >= 0.70 → rows at thresholds 0.50, 0.70, 0.90.
        # Lowest FNR among them is 0.25 at threshold 0.50.
        row = common.get_high_sensitivity_row(threshold_df, min_precision=0.70)
        assert row["Threshold"].iloc[0] == 0.50

    def test_min_precision_zero_picks_lowest_fnr_overall(self, threshold_df):
        # All rows pass min_precision=0; lowest FNR is 0.01 at threshold 0.10.
        row = common.get_high_sensitivity_row(threshold_df, min_precision=0.0)
        assert row["Threshold"].iloc[0] == 0.10

    def test_falls_back_when_no_candidates_meet_precision(self, threshold_df):
        # No row has Precision >= 2.0 → fallback uses the full df.
        # Lowest FNR overall is at threshold 0.10.
        row = common.get_high_sensitivity_row(threshold_df, min_precision=2.0)
        assert row["Threshold"].iloc[0] == 0.10
