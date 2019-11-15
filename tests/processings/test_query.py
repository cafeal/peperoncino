import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
import pupil as pp


class TestQuery:
    @pytest.mark.parametrize(
        "query", ["a == 1", pytest.param("x == 1", marks=pytest.mark.xfail)]
    )
    def test_process(self, query):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

        proc = pp.Query(query)

        (df,) = proc.process([df])
        assert_frame_equal(df, pd.DataFrame({"a": [1], "b": [4]}))
