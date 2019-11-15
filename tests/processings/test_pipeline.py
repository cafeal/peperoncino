import pandas as pd
from pandas.testing import assert_frame_equal
import pupil as pp


class RenameProcessing(pp.SeparatedProcessing):
    def __init__(self):
        super().__init__(is_fixed_columns=False)

    def sep_process(self, df):
        return df.rename(columns={"a": "A"})


class DoubleProcessing(pp.SeparatedProcessing):
    def __init__(self):
        super().__init__(is_fixed_rows=False)

    def sep_process(self, df):
        return pd.concat((df, df), ignore_index=True)


class TestPipeline:
    def test_process(self):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

        proc = pp.Pipeline(RenameProcessing(), DoubleProcessing())

        (df,) = proc.process([df])

        assert_frame_equal(
            df, pd.DataFrame({"A": [1, 2, 3, 1, 2, 3], "b": [4, 5, 6, 4, 5, 6]})
        )
