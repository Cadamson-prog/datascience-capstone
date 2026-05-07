"""Unit tests for src/utils/logreg.py"""

import numpy as np
import pandas as pd
import pytest

from src.utils import logreg


EPS = 1e-6  # Mirrors the constant inside engineer_features_logistic


@pytest.fixture
def full_logreg_df():
    """A DataFrame with id/label cols plus every direct, confounder, and
    extra element used by `engineer_features_logistic`."""
    return pd.DataFrame(
        {
            # excluded id/label columns
            "stub_id":      [1, 1, 2, 2],
            "particle_id":  [1, 2, 3, 4],
            "label":        ["GSR", "Non_GSR", "GSR", "Non_GSR"],
            "target":       [1, 0, 1, 0],
            # direct GSR elements
            "pb": [10.0, 5.0, 8.0, 0.0],
            "ba": [3.0, 7.0, 1.0, 4.0],
            "sb": [5.0, 3.0, 0.0, 2.0],
            # confounders
            "zn": [2.0, 1.0, 4.0, 1.0],
            "cu": [1.0, 0.0, 2.0, 1.0],
            "ti": [3.0, 2.0, 0.0, 1.0],
            # extra element (not in direct/confounder lists, but still numeric
            # and not in non_feature_cols → counts toward total_mass / diversity)
            "fe": [4.0, 3.0, 5.0, 2.0],
        }
    )


# ---------------------------------------------------------------------------
# Output-shape / no-mutation invariants
# ---------------------------------------------------------------------------
class TestOutputAndNoMutation:

    def test_returns_new_dataframe_with_original_columns_intact(self, full_logreg_df):
        out = logreg.engineer_features_logistic(full_logreg_df)
        assert isinstance(out, pd.DataFrame)
        # All original columns survive in the output
        for col in full_logreg_df.columns:
            assert col in out.columns
            np.testing.assert_array_equal(out[col].values, full_logreg_df[col].values)

    def test_original_dataframe_not_mutated(self, full_logreg_df):
        snapshot = full_logreg_df.copy(deep=True)
        logreg.engineer_features_logistic(full_logreg_df)
        pd.testing.assert_frame_equal(full_logreg_df, snapshot)

    def test_row_count_unchanged(self, full_logreg_df):
        out = logreg.engineer_features_logistic(full_logreg_df)
        assert len(out) == len(full_logreg_df)


# ---------------------------------------------------------------------------
# Log transforms
# ---------------------------------------------------------------------------
class TestLogTransforms:

    @pytest.mark.parametrize("col", ["pb", "ba", "sb", "zn", "cu", "ti"])
    def test_log_column_present(self, full_logreg_df, col):
        out = logreg.engineer_features_logistic(full_logreg_df)
        assert f"log_{col}" in out.columns

    def test_log_value_matches_log1p(self, full_logreg_df):
        out = logreg.engineer_features_logistic(full_logreg_df)
        np.testing.assert_allclose(
            out["log_pb"].values, np.log1p(full_logreg_df["pb"].values)
        )

    def test_log_column_skipped_when_source_missing(self, full_logreg_df):
        df = full_logreg_df.drop(columns=["pb"])
        out = logreg.engineer_features_logistic(df)
        assert "log_pb" not in out.columns
        # ratios/interactions that depend on pb should also be absent
        assert "log_pb_ba_ratio" not in out.columns
        assert "log_pb_sb_ratio" not in out.columns
        assert "log_pb_zn_ratio" not in out.columns
        assert "pb_sb_interaction" not in out.columns
        assert "pb_ba_interaction" not in out.columns


# ---------------------------------------------------------------------------
# Ratios (GSR-element pairs and GSR vs confounder pairs)
# ---------------------------------------------------------------------------
class TestRatios:

    def test_pb_ba_ratio_value(self, full_logreg_df):
        out = logreg.engineer_features_logistic(full_logreg_df)
        expected = np.log1p(full_logreg_df["pb"] / (full_logreg_df["ba"] + EPS))
        np.testing.assert_allclose(out["log_pb_ba_ratio"].values, expected.values)

    def test_all_gsr_pair_ratios_present(self, full_logreg_df):
        out = logreg.engineer_features_logistic(full_logreg_df)
        for col in ("log_pb_ba_ratio", "log_pb_sb_ratio", "log_ba_sb_ratio"):
            assert col in out.columns

    def test_all_confounder_ratios_present(self, full_logreg_df):
        out = logreg.engineer_features_logistic(full_logreg_df)
        for col in ("log_pb_zn_ratio", "log_sb_cu_ratio", "log_ba_ti_ratio"):
            assert col in out.columns

    def test_ratio_skipped_when_either_input_missing(self, full_logreg_df):
        df = full_logreg_df.drop(columns=["zn"])
        out = logreg.engineer_features_logistic(df)
        assert "log_pb_zn_ratio" not in out.columns


# ---------------------------------------------------------------------------
# Domain summary features
# ---------------------------------------------------------------------------
class TestDomainSummary:

    def test_log_gsr_over_confounders_value(self, full_logreg_df):
        out = logreg.engineer_features_logistic(full_logreg_df)
        gsr = full_logreg_df[["pb", "ba", "sb"]].sum(axis=1)
        conf = full_logreg_df[["zn", "cu", "ti"]].sum(axis=1)
        expected = np.log1p(gsr / (conf + EPS))
        np.testing.assert_allclose(out["log_gsr_over_confounders"].values, expected.values)

    def test_log_gsr_over_confounders_skipped_when_no_confounders(self, full_logreg_df):
        df = full_logreg_df.drop(columns=["zn", "cu", "ti"])
        out = logreg.engineer_features_logistic(df)
        assert "log_gsr_over_confounders" not in out.columns

    def test_pct_columns_exist_for_every_element(self, full_logreg_df):
        out = logreg.engineer_features_logistic(full_logreg_df)
        for col in ("pb", "ba", "sb", "zn", "cu", "ti", "fe"):
            assert f"{col}_pct" in out.columns

    def test_pct_columns_sum_to_about_one_per_row(self, full_logreg_df):
        out = logreg.engineer_features_logistic(full_logreg_df)
        pct_cols = [c for c in out.columns if c.endswith("_pct")]
        # The eps in the denominator pushes the row sum just below 1.0.
        np.testing.assert_allclose(out[pct_cols].sum(axis=1).values, 1.0, atol=1e-5)

    def test_pct_value_matches_share_of_total_mass(self, full_logreg_df):
        out = logreg.engineer_features_logistic(full_logreg_df)
        element_cols = ["pb", "ba", "sb", "zn", "cu", "ti", "fe"]
        total = full_logreg_df[element_cols].sum(axis=1) + EPS
        np.testing.assert_allclose(
            out["pb_pct"].values, (full_logreg_df["pb"] / total).values
        )

    def test_id_columns_excluded_from_pct_features(self, full_logreg_df):
        out = logreg.engineer_features_logistic(full_logreg_df)
        # `target` is numeric and would otherwise be picked up by select_dtypes,
        # but the function explicitly excludes it via `non_feature_cols`.
        assert "target_pct" not in out.columns
        assert "particle_id_pct" not in out.columns
        assert "stub_id_pct" not in out.columns


# ---------------------------------------------------------------------------
# Interaction terms
# ---------------------------------------------------------------------------
class TestInteractions:

    @pytest.mark.parametrize(
        "feature, a, b",
        [
            ("pb_sb_interaction", "pb", "sb"),
            ("ba_sb_interaction", "ba", "sb"),
            ("pb_ba_interaction", "pb", "ba"),
        ],
    )
    def test_interaction_value(self, full_logreg_df, feature, a, b):
        out = logreg.engineer_features_logistic(full_logreg_df)
        np.testing.assert_allclose(
            out[feature].values, (full_logreg_df[a] * full_logreg_df[b]).values
        )


# ---------------------------------------------------------------------------
# Diversity column
# ---------------------------------------------------------------------------
class TestElementDiversity:

    def test_diversity_counts_nonzero_elements_per_row(self, full_logreg_df):
        out = logreg.engineer_features_logistic(full_logreg_df)
        # 7 element columns total: pb, ba, sb, zn, cu, ti, fe
        # Row 0: all 7 nonzero
        # Row 1: cu is 0 → 6
        # Row 2: sb and ti are 0 → 5
        # Row 3: pb is 0 → 6
        np.testing.assert_array_equal(out["element_diversity"].values, [7, 6, 5, 6])

    def test_diversity_excludes_id_and_label_columns(self):
        # Even though `target` is numeric, it should NOT contribute to diversity.
        df = pd.DataFrame({"target": [1, 1, 0], "pb": [1.0, 0.0, 0.0]})
        out = logreg.engineer_features_logistic(df)
        np.testing.assert_array_equal(out["element_diversity"].values, [1, 0, 0])
