import pytest
from pandas.testing import assert_frame_equal
import pandas as pd
import pupil as pp


class TestSelet:
    @pytest.mark.parametrize(
        "cols,lackable_cols",
        [
            (["a", "b"], []),
            (["a", "b", "d"], ["d"]),
            pytest.param(["a", "b", "d"], [], marks=pytest.mark.xfail),
        ],
    )
    def test_process(self, cols, lackable_cols):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
        proc = pp.Select(cols, lackable_cols=lackable_cols)
        (df,) = proc.process([df])
        assert_frame_equal(df, pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
