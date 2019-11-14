import pandas as pd
import pupil as pp


class TestRenameColumns:
    def test_process(self):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
        proc = pp.RenameColumns({"b": "B"}, c="C")
        (df,) = proc.process([df])
        assert df.equals(pd.DataFrame({"a": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]}))
