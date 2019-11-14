import pytest
import pandas as pd
import pupil as pp


class TestDropColumns:
    @pytest.mark.parametrize(
        "cols", [["b", "c"], pytest.param(["b", "c", "d"], marks=pytest.mark.xfail)]
    )
    def test_process(self, cols):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
        proc = pp.DropColumns(cols)
        (df,) = proc.process([df])
        assert df.equals(pd.DataFrame({"a": [1, 2, 3]}))
