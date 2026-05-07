"""Unit tests for src/utils/nn.py"""

import numpy as np
import pandas as pd
import pytest

from src.utils import nn


# ---------------------------------------------------------------------------
# multiplicative_replacement
# ---------------------------------------------------------------------------
class TestMultiplicativeReplacement:
    """
    `multiplicative_replacement` replaces zeros with delta and rescales the
    nonzero entries so each row's total mass is preserved.
    """

    def test_no_zeros_returns_unchanged_values(self):
        X = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        out = nn.multiplicative_replacement(X)
        np.testing.assert_allclose(out, X)

    def test_explicit_delta_replaces_zeros(self):
        X = np.array([[10.0, 0.0, 0.0]])
        out = nn.multiplicative_replacement(X, delta=0.1)
        # zeros become 0.1; row sum stays 10.0
        assert out[0, 1] == pytest.approx(0.1)
        assert out[0, 2] == pytest.approx(0.1)
        assert out.sum(axis=1)[0] == pytest.approx(10.0)

    def test_row_sum_is_preserved(self):
        X = np.array([[10.0, 5.0, 0.0, 5.0], [0.0, 8.0, 2.0, 0.0]])
        original_sums = X.sum(axis=1)
        out = nn.multiplicative_replacement(X)
        np.testing.assert_allclose(out.sum(axis=1), original_sums, rtol=1e-10)

    def test_default_delta_is_half_of_min_nonzero(self):
        X = np.array([[4.0, 2.0, 0.0]])
        out = nn.multiplicative_replacement(X)
        # min nonzero in matrix is 2.0 → delta = 1.0
        assert out[0, 2] == pytest.approx(1.0)

    def test_all_zero_row_left_unchanged(self):
        X = np.array([[0.0, 0.0, 0.0], [1.0, 2.0, 3.0]])
        out = nn.multiplicative_replacement(X)
        # all-zero row stays all zeros (row_sum gate prevents replacement)
        np.testing.assert_array_equal(out[0], [0.0, 0.0, 0.0])

    def test_does_not_mutate_input(self):
        X = np.array([[1.0, 0.0, 2.0]])
        X_before = X.copy()
        nn.multiplicative_replacement(X, delta=0.1)
        np.testing.assert_array_equal(X, X_before)

    def test_returns_float_dtype(self):
        X = np.array([[1, 2, 0], [3, 0, 4]], dtype=int)
        out = nn.multiplicative_replacement(X)
        assert np.issubdtype(out.dtype, np.floating)


# ---------------------------------------------------------------------------
# clr_transform
# ---------------------------------------------------------------------------
class TestClrTransform:
    """`clr_transform` returns log(X) - mean(log(X), axis=1, keepdims=True)."""

    def test_each_row_sums_to_zero(self):
        rng = np.random.default_rng(0)
        X = rng.uniform(0.1, 10.0, size=(5, 6))
        out = nn.clr_transform(X)
        np.testing.assert_allclose(out.sum(axis=1), 0.0, atol=1e-10)

    def test_specific_value(self):
        # Two-element row [a, b]: CLR[0] = log(a) - (log(a)+log(b))/2
        X = np.array([[np.e, 1.0]])  # log(e)=1, log(1)=0, mean=0.5
        out = nn.clr_transform(X)
        np.testing.assert_allclose(out, [[0.5, -0.5]], atol=1e-10)

    def test_constant_row_yields_zeros(self):
        # All values equal → every entry equals the row mean → CLR is zero.
        X = np.full((1, 4), 7.0)
        out = nn.clr_transform(X)
        np.testing.assert_allclose(out, np.zeros((1, 4)), atol=1e-10)

    def test_output_shape_matches_input(self):
        X = np.array([[1.0, 2.0, 3.0, 4.0]])
        assert nn.clr_transform(X).shape == X.shape


# ---------------------------------------------------------------------------
# engineer_nn_features
#
# Feature layout: hstack of [CLR(X), presence(X), pb_sb_ratio_col, log_pb_sb_col]
# → output has 2*len(element_cols) + 2 columns, dtype float32.
# Requires `pb`, `sb`, `ba`, `o` columns to be present in df.
# ---------------------------------------------------------------------------
@pytest.fixture
def small_nn_df():
    return pd.DataFrame(
        {
            "pb": [10.0, 0.0, 5.0],
            "sb": [5.0, 0.0, 3.0],
            "ba": [3.0, 50.0, 2.0],
            "o":  [10.0, 30.0, 5.0],
            "fe": [2.0, 1.0, 0.5],
        }
    )


class TestEngineerNnFeatures:

    def test_output_shape(self, small_nn_df):
        cols = ["pb", "sb", "ba", "o", "fe"]
        out = nn.engineer_nn_features(small_nn_df, cols)
        # 2 * len(cols) (CLR + presence) + 2 (ratio + log) = 12
        assert out.shape == (3, 12)

    def test_output_dtype_is_float32(self, small_nn_df):
        cols = ["pb", "sb", "ba", "o", "fe"]
        out = nn.engineer_nn_features(small_nn_df, cols)
        assert out.dtype == np.float32

    def test_presence_columns_match_raw_indicator(self, small_nn_df):
        cols = ["pb", "sb", "ba", "o", "fe"]
        out = nn.engineer_nn_features(small_nn_df, cols)
        # Presence cols sit immediately after the CLR cols.
        n = len(cols)
        presence = out[:, n : 2 * n]
        expected = (small_nn_df[cols].values > 0).astype(np.float32)
        np.testing.assert_array_equal(presence, expected)

    def test_log_pb_sb_column(self, small_nn_df):
        cols = ["pb", "sb", "ba", "o", "fe"]
        out = nn.engineer_nn_features(small_nn_df, cols)
        log_pb_sb = out[:, -1]
        expected = np.log1p(small_nn_df["pb"].values + small_nn_df["sb"].values).astype(
            np.float32
        )
        np.testing.assert_allclose(log_pb_sb, expected, rtol=1e-6)

    def test_pb_sb_ratio_uses_sentinel_when_denominator_is_zero(self):
        # Build a row where total_mass - ba - o == 0 to trigger the
        # sentinel (-1) branch in the ratio computation.
        df = pd.DataFrame(
            {
                "pb": [3.0],
                "sb": [2.0],
                "ba": [4.0],
                "o":  [1.0],
            }
        )
        # element_cols only includes ba and o, so total_mass = ba+o = 5,
        # denom = total_mass - ba - o = 0 → safe_denom = -1, so
        # pb_sb_ratio = (3 + 2) / -1 = -5
        cols = ["ba", "o"]
        out = nn.engineer_nn_features(df, cols)
        ratio_col = out[:, -2]
        assert ratio_col[0] == pytest.approx(-5.0)


# ---------------------------------------------------------------------------
# build_feature_matrix
# ---------------------------------------------------------------------------
@pytest.fixture
def nn_and_raw_dfs():
    df_nn = pd.DataFrame(
        {
            "a": [1.0, 2.0, 3.0],
            "b": [4.0, 5.0, 6.0],
            "extra": [7.0, 8.0, 9.0],
        }
    )
    df_raw = pd.DataFrame(
        {
            "a": [10.0, 20.0, 30.0],
            "b": [40.0, 50.0, 60.0],
        }
    )
    return df_nn, df_raw


class TestBuildFeatureMatrix:

    def test_source_nn_pulls_from_nn_dataframe(self, nn_and_raw_dfs):
        df_nn, df_raw = nn_and_raw_dfs
        cfg = {"source": "nn", "cols": ["a", "b"]}
        out = nn.build_feature_matrix(cfg, df_nn, df_raw, [0, 2])
        np.testing.assert_array_equal(out, [[1.0, 4.0], [3.0, 6.0]])

    def test_source_raw_pulls_from_raw_dataframe(self, nn_and_raw_dfs):
        df_nn, df_raw = nn_and_raw_dfs
        cfg = {"source": "raw", "cols": ["a"]}
        out = nn.build_feature_matrix(cfg, df_nn, df_raw, [0, 1])
        np.testing.assert_array_equal(out, [[10.0], [20.0]])

    def test_extra_from_nn_appends_columns(self, nn_and_raw_dfs):
        df_nn, df_raw = nn_and_raw_dfs
        cfg = {"source": "raw", "cols": ["a"], "extra_from_nn": ["extra"]}
        out = nn.build_feature_matrix(cfg, df_nn, df_raw, [0])
        # raw 'a' at index 0 is 10.0; nn 'extra' at index 0 is 7.0
        np.testing.assert_array_equal(out, [[10.0, 7.0]])

    def test_no_extra_key_works(self, nn_and_raw_dfs):
        df_nn, df_raw = nn_and_raw_dfs
        cfg = {"source": "nn", "cols": ["a"]}  # no 'extra_from_nn' key
        out = nn.build_feature_matrix(cfg, df_nn, df_raw, [1])
        np.testing.assert_array_equal(out, [[2.0]])

    def test_empty_extra_list_skips_hstack(self, nn_and_raw_dfs):
        df_nn, df_raw = nn_and_raw_dfs
        cfg = {"source": "nn", "cols": ["a", "b"], "extra_from_nn": []}
        out = nn.build_feature_matrix(cfg, df_nn, df_raw, [0, 1, 2])
        assert out.shape == (3, 2)

    def test_output_dtype_is_float32(self, nn_and_raw_dfs):
        df_nn, df_raw = nn_and_raw_dfs
        cfg = {"source": "nn", "cols": ["a"]}
        out = nn.build_feature_matrix(cfg, df_nn, df_raw, [0])
        assert out.dtype == np.float32
