import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
import pupil as pp


class TestDropDuplicates:
    @pytest.mark.parametrize(
        "cols",
        [None, ["b", "c"], pytest.param(["b", "c", "d"], marks=pytest.mark.xfail)],
    )
    def test_process(self, cols):
        df = pd.DataFrame({"a": [1, 2, 3, 3], "b": [4, 5, 5, 5], "c": [5, 6, 6, 6]})
        proc = pp.DropDuplicates(cols)
        (df,) = proc.process([df])

        if cols is None:
            assert_frame_equal(
                df, pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 5], "c": [5, 6, 6]})
            )
        else:
            assert_frame_equal(
                df, pd.DataFrame({"a": [1, 2], "b": [4, 5], "c": [5, 6]})
            )
