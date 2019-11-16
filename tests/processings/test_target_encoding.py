import pytest
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import pupil as pp


class TestTargetEncoding:
    @pytest.mark.parametrize(
        "prior_weight,impute_by_prior",
        [(0.0, False), (1.0, False), (0.0, True), (1.0, True)],
    )
    def test_process(self, prior_weight, impute_by_prior):
        ref_df = pd.DataFrame(
            {
                "a": [1, 1, 2, 2, 3, 3],
                "b": [4, 4, 4, 5, 5, 5],
                "y": [1, 2, 3, 4, 5, 6],
                "fold": [1, 2, 1, 1, 2, 2],
            },
            index=[10, 20, 30, 40, 50, 60],
        )

        other_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

        proc = pp.TargetEncoding(
            ["a", "b"],
            "y",
            ref=0,
            prior_weight=prior_weight,
            impute_by_prior=impute_by_prior,
        )

        ref_df, other_df = proc.process([ref_df, other_df])

        prior = (1 + 2 + 3 + 4 + 5 + 6) / 6

        mapping = {
            (1, 4): (1 + 2) / 2,
            (2, 4): 3.0 / 1,
            (2, 5): 4.0 / 1,
            (3, 5): (5 + 6) / 2,
        }
        if prior_weight > 0.0:
            lamb = 2 / (2 + prior_weight)
            mapping[(1, 4)] = lamb * mapping[(1, 4)] + (1 - lamb) * prior

            lamb = 1 / (1 + prior_weight)
            mapping[(2, 4)] = lamb * mapping[(2, 4)] + (1 - lamb) * prior

            lamb = 1 / (1 + prior_weight)
            mapping[(2, 5)] = lamb * mapping[(2, 5)] + (1 - lamb) * prior

            lamb = 2 / (2 + prior_weight)
            mapping[(3, 5)] = lamb * mapping[(3, 5)] + (1 - lamb) * prior

        xref_df = pd.DataFrame(
            {
                "a": [1, 1, 2, 2, 3, 3],
                "b": [4, 4, 4, 5, 5, 5],
                "y": [1, 2, 3, 4, 5, 6],
                "fold": [1, 2, 1, 1, 2, 2],
                "TARGET_ENC_a&b_BY_y": [
                    mapping[(1, 4)],
                    mapping[(1, 4)],
                    mapping[(2, 4)],
                    mapping[(2, 5)],
                    mapping[(3, 5)],
                    mapping[(3, 5)],
                ],
            },
            index=[10, 20, 30, 40, 50, 60],
        )
        assert_frame_equal(ref_df, xref_df)

        xother_df = pd.DataFrame(
            {
                "a": [1, 2, 3],
                "b": [4, 5, 6],
                "TARGET_ENC_a&b_BY_y": [
                    mapping[(1, 4)],
                    mapping[(2, 5)],
                    prior if impute_by_prior else np.nan,
                ],
            },
        )
        assert_frame_equal(other_df, xother_df)
