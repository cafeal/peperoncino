import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
import peperoncino as pp


class TestApplyColumn:
    @pytest.mark.parametrize(
        "col, fn",
        [
            ("a", lambda x: x * 2),
            pytest.param("x", lambda x: x * 2, marks=pytest.mark.xfail),
        ],
    )
    def test_process(self, col, fn):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        proc = pp.ApplyColumn(col, fn)
        (df,) = proc.process([df])

        assert_frame_equal(df, pd.DataFrame({"a": [2, 4, 6], "b": [4, 5, 6]}))
