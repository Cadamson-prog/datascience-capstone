"""Unit tests for src/utils/nist.py"""

import numpy as np
import pandas as pd
import pytest

from src.utils import nist


# ---------------------------------------------------------------------------
# extract_class
# ---------------------------------------------------------------------------
class TestExtractClass:
    """`extract_class` pulls the bracketed prefix from a NIST class string."""

    def test_standard_classification_string(self):
        assert nist.extract_class("[Aluminosilicate: 0.95]") == "Aluminosilicate"

    def test_class_with_spaces_and_hyphens(self):
        assert nist.extract_class("[Pb-Ba: 0.7]") == "Pb-Ba"

    def test_no_bracket_returns_unknown(self):
        assert nist.extract_class("plain text") == "Unknown"

    def test_no_colon_returns_unknown(self):
        # The regex requires a `:` after the class name
        assert nist.extract_class("[NoColon]") == "Unknown"

    def test_first_match_wins(self):
        # Two bracketed segments; only the first should be returned.
        assert nist.extract_class("[First: x] [Second: y]") == "First"

    def test_non_string_input_is_coerced(self):
        # Function calls str(s); None has no bracket → "Unknown"
        assert nist.extract_class(None) == "Unknown"

    def test_numeric_input_coerced_to_string(self):
        # str(123) has no bracket → "Unknown"
        assert nist.extract_class(123) == "Unknown"


# ---------------------------------------------------------------------------
# label_gsr
# ---------------------------------------------------------------------------
class TestLabelGsr:
    """`label_gsr` maps a class name to GSR / Non_GSR / Low_Quality."""

    @pytest.mark.parametrize(
        "class_name", ["GSR", "gsr", "Classic GSR", "GSR-like", "Char GSR-like"]
    )
    def test_anything_with_gsr_substring_labels_gsr(self, class_name):
        assert nist.label_gsr(class_name) == "GSR"

    @pytest.mark.parametrize(
        "class_name", ["#Unclassified#", "lowcounts", "Low Counts", "LOWCOUNTS"]
    )
    def test_low_quality_classes(self, class_name):
        assert nist.label_gsr(class_name) == "Low_Quality"

    @pytest.mark.parametrize(
        "class_name", ["Iron-bearing", "Ca-bearing", "Silicate", "Pb-Ba", "Brass"]
    )
    def test_other_classes_label_non_gsr(self, class_name):
        assert nist.label_gsr(class_name) == "Non_GSR"

    def test_empty_string_labels_non_gsr(self):
        # No 'gsr' substring, not in low-quality list → Non_GSR
        assert nist.label_gsr("") == "Non_GSR"


# ---------------------------------------------------------------------------
# renormalize_with_oxygen
#
# The function scales non-oxygen columns by (100 - oxygen) / 100, so that
# row totals (oxygen + non-oxygen) sum to ~100 when oxygen is included.
# Note: the implementation modifies the input DataFrame in place. Tests
# pass freshly-built DataFrames to avoid cross-test contamination.
# ---------------------------------------------------------------------------
class TestRenormalizeWithOxygen:

    def test_scales_non_oxygen_cols_by_expected_factor(self):
        df = pd.DataFrame(
            {
                "o":  [20.0],
                "pb": [40.0],
                "sb": [40.0],
            }
        )
        out = nist.renormalize_with_oxygen(df, ["pb", "sb"])
        # scale = (100 - 20) / 100 = 0.8
        assert out["pb"].iloc[0] == pytest.approx(32.0)
        assert out["sb"].iloc[0] == pytest.approx(32.0)

    def test_oxygen_column_left_untouched(self):
        df = pd.DataFrame({"o": [25.0], "pb": [50.0], "sb": [25.0]})
        out = nist.renormalize_with_oxygen(df, ["pb", "sb"])
        assert out["o"].iloc[0] == 25.0

    def test_row_totals_sum_to_100_when_input_summed_to_100(self):
        # If the original (non-oxygen) row already sums to 100, the rescaled
        # row + oxygen should sum to 100.
        df = pd.DataFrame({"o": [30.0], "pb": [60.0], "sb": [40.0]})
        out = nist.renormalize_with_oxygen(df, ["pb", "sb"])
        total = out["o"].iloc[0] + out["pb"].iloc[0] + out["sb"].iloc[0]
        assert total == pytest.approx(100.0)

    def test_multiple_rows_use_per_row_oxygen_scale(self):
        df = pd.DataFrame(
            {
                "o":  [10.0, 50.0],
                "pb": [50.0, 50.0],
                "sb": [50.0, 50.0],
            }
        )
        out = nist.renormalize_with_oxygen(df, ["pb", "sb"])
        # Row 0: scale = 0.9 → 50 * 0.9 = 45
        # Row 1: scale = 0.5 → 50 * 0.5 = 25
        np.testing.assert_allclose(out["pb"].values, [45.0, 25.0])
        np.testing.assert_allclose(out["sb"].values, [45.0, 25.0])

    def test_custom_oxygen_column_name(self):
        df = pd.DataFrame({"OXY": [20.0], "pb": [40.0]})
        out = nist.renormalize_with_oxygen(df, ["pb"], oxygen_col="OXY")
        assert out["pb"].iloc[0] == pytest.approx(32.0)

    def test_zero_oxygen_leaves_values_unchanged(self):
        df = pd.DataFrame({"o": [0.0], "pb": [42.0]})
        out = nist.renormalize_with_oxygen(df, ["pb"])
        # scale = 1.0
        assert out["pb"].iloc[0] == pytest.approx(42.0)

    def test_oxygen_at_100_zeros_out_other_columns(self):
        df = pd.DataFrame({"o": [100.0], "pb": [42.0], "sb": [10.0]})
        out = nist.renormalize_with_oxygen(df, ["pb", "sb"])
        assert out["pb"].iloc[0] == pytest.approx(0.0)
        assert out["sb"].iloc[0] == pytest.approx(0.0)
