import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import pupil as pp


class TestStatsEncoding:
    def test_process(self):
        ref_df = pd.DataFrame(
            {
                "a": [1, 1, 2, 2, 3, 3],
                "b": [4, 4, 4, 5, 5, 5],
                "y": [1, 2, 3, 4, 5, 6],
                "fold": [1, 2, 1, 1, 2, 2],
            },
            index=[10, 20, 30, 40, 50, 60],
        )

        other_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 5]})

        proc = pp.StatsEncoding(["a", "b"], "y", ["mean", "var"], ref=0)

        ref_df, other_df = proc.process([ref_df, other_df])

        xref_df = pd.DataFrame(
            {
                "a": [1, 1, 2, 2, 3, 3],
                "b": [4, 4, 4, 5, 5, 5],
                "y": [1, 2, 3, 4, 5, 6],
                "fold": [1, 2, 1, 1, 2, 2],
                "STATS_ENC_a&b_BY_mean_y": [
                    (1 + 2) / 2,
                    (1 + 2) / 2,
                    3.0 / 1,
                    4.0 / 1,
                    (5 + 6) / 2,
                    (5 + 6) / 2,
                ],
                "STATS_ENC_a&b_BY_var_y": [
                    ((1 - 1.5) ** 2 + (2 - 1.5) ** 2) / (2 - 1),
                    ((1 - 1.5) ** 2 + (2 - 1.5) ** 2) / (2 - 1),
                    np.nan,
                    np.nan,
                    ((5 - 5.5) ** 2 + (6 - 5.5) ** 2) / (2 - 1),
                    ((5 - 5.5) ** 2 + (6 - 5.5) ** 2) / (2 - 1),
                ],
            },
            index=[10, 20, 30, 40, 50, 60],
        )
        assert_frame_equal(ref_df, xref_df)

        xother_df = pd.DataFrame(
            {
                "a": [1, 2, 3],
                "b": [4, 5, 5],
                "STATS_ENC_a&b_BY_mean_y": [(1 + 2) / 2, 4, (5 + 6) / 2],
                "STATS_ENC_a&b_BY_var_y": [
                    ((1 - 1.5) ** 2 + (2 - 1.5) ** 2) / (2 - 1),
                    np.nan,
                    ((5 - 5.5) ** 2 + (6 - 5.5) ** 2) / (2 - 1),
                ],
            },
        )
        assert_frame_equal(other_df, xother_df)
