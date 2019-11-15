import pandas as pd
from pandas.testing import assert_frame_equal
import pupil as pp


class TestRenameColumns:
    def test_process(self):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
        proc = pp.RenameColumns({"b": "B"}, c="C")
        (df,) = proc.process([df])
        assert_frame_equal(
            df, pd.DataFrame({"a": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
        )
