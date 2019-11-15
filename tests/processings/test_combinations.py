import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

import pupil as pp


class TestCombinations:
    @pytest.mark.parametrize(
        "comb_type",
        [
            "combinations",
            "combinations_with_replacement",
            "product",
            "permutations",
            pytest.param("xxx", marks=pytest.mark.xfail),
        ],
    )
    def test_process(self, comb_type):
        df = pd.DataFrame(
            {"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9], "d": [10, 11, 12]}
        )
        proc = pp.Combinations(["a", "b", "c"], ["*", "/"], comb_type=comb_type)

        if comb_type == "combinations":
            (df,) = proc.process([df])
            assert_frame_equal(
                df,
                pd.DataFrame(
                    {
                        "a": [1, 2, 3],
                        "b": [4, 5, 6],
                        "c": [7, 8, 9],
                        "d": [10, 11, 12],
                        "*_a_b": [1 * 4, 2 * 5, 3 * 6],
                        "/_a_b": [1 / 4, 2 / 5, 3 / 6],
                        "*_a_c": [1 * 7, 2 * 8, 3 * 9],
                        "/_a_c": [1 / 7, 2 / 8, 3 / 9],
                        "*_b_c": [4 * 7, 5 * 8, 6 * 9],
                        "/_b_c": [4 / 7, 5 / 8, 6 / 9],
                    }
                ),
            )
        elif comb_type == "combinations_with_replacement":
            (df,) = proc.process([df])
            assert_frame_equal(
                df,
                pd.DataFrame(
                    {
                        "a": [1, 2, 3],
                        "b": [4, 5, 6],
                        "c": [7, 8, 9],
                        "d": [10, 11, 12],
                        "*_a_a": [1 * 1, 2 * 2, 3 * 3],
                        "/_a_a": [1 / 1, 2 / 2, 3 / 3],
                        "*_a_b": [1 * 4, 2 * 5, 3 * 6],
                        "/_a_b": [1 / 4, 2 / 5, 3 / 6],
                        "*_a_c": [1 * 7, 2 * 8, 3 * 9],
                        "/_a_c": [1 / 7, 2 / 8, 3 / 9],
                        "*_b_b": [4 * 4, 5 * 5, 6 * 6],
                        "/_b_b": [4 / 4, 5 / 5, 6 / 6],
                        "*_b_c": [4 * 7, 5 * 8, 6 * 9],
                        "/_b_c": [4 / 7, 5 / 8, 6 / 9],
                        "*_c_c": [7 * 7, 8 * 8, 9 * 9],
                        "/_c_c": [7 / 7, 8 / 8, 9 / 9],
                    }
                ),
            )
        elif comb_type == "product":
            (df,) = proc.process([df])
            assert_frame_equal(
                df,
                pd.DataFrame(
                    {
                        "a": [1, 2, 3],
                        "b": [4, 5, 6],
                        "c": [7, 8, 9],
                        "d": [10, 11, 12],
                        "*_a_a": [1 * 1, 2 * 2, 3 * 3],
                        "/_a_a": [1 / 1, 2 / 2, 3 / 3],
                        "*_a_b": [1 * 4, 2 * 5, 3 * 6],
                        "/_a_b": [1 / 4, 2 / 5, 3 / 6],
                        "*_a_c": [1 * 7, 2 * 8, 3 * 9],
                        "/_a_c": [1 / 7, 2 / 8, 3 / 9],
                        "*_b_a": [4 * 1, 5 * 2, 6 * 3],
                        "/_b_a": [4 / 1, 5 / 2, 6 / 3],
                        "*_b_b": [4 * 4, 5 * 5, 6 * 6],
                        "/_b_b": [4 / 4, 5 / 5, 6 / 6],
                        "*_b_c": [4 * 7, 5 * 8, 6 * 9],
                        "/_b_c": [4 / 7, 5 / 8, 6 / 9],
                        "*_c_a": [7 * 1, 8 * 2, 9 * 3],
                        "/_c_a": [7 / 1, 8 / 2, 9 / 3],
                        "*_c_b": [7 * 4, 8 * 5, 9 * 6],
                        "/_c_b": [7 / 4, 8 / 5, 9 / 6],
                        "*_c_c": [7 * 7, 8 * 8, 9 * 9],
                        "/_c_c": [7 / 7, 8 / 8, 9 / 9],
                    }
                ),
            )
        elif comb_type == "permutations":
            (df,) = proc.process([df])

            assert_frame_equal(
                df,
                pd.DataFrame(
                    {
                        "a": [1, 2, 3],
                        "b": [4, 5, 6],
                        "c": [7, 8, 9],
                        "d": [10, 11, 12],
                        "*_a_b": [1 * 4, 2 * 5, 3 * 6],
                        "/_a_b": [1 / 4, 2 / 5, 3 / 6],
                        "*_a_c": [1 * 7, 2 * 8, 3 * 9],
                        "/_a_c": [1 / 7, 2 / 8, 3 / 9],
                        "*_b_a": [4 * 1, 5 * 2, 6 * 3],
                        "/_b_a": [4 / 1, 5 / 2, 6 / 3],
                        "*_b_c": [4 * 7, 5 * 8, 6 * 9],
                        "/_b_c": [4 / 7, 5 / 8, 6 / 9],
                        "*_c_a": [7 * 1, 8 * 2, 9 * 3],
                        "/_c_a": [7 / 1, 8 / 2, 9 / 3],
                        "*_c_b": [7 * 4, 8 * 5, 9 * 6],
                        "/_c_b": [7 / 4, 8 / 5, 9 / 6],
                    }
                ),
            )
