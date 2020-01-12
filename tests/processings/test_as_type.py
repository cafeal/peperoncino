import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
import peperoncino as pp


class TestAsType:
    @pytest.mark.parametrize("dtype", ["int64", "Int64", "float64", "object"])
    def test_processing(self, dtype):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

        proc = pp.AsType({"a": dtype})
        (df,) = proc.process([df])

        xdf = df.copy()
        xdf.a = xdf.a.astype(dtype)
        assert_frame_equal(df, xdf)

    def test_processing_datetime(self):
        df = pd.DataFrame(
            {
                "a": [1, 2, 3],
                "b": [
                    "2020-01-01 00:00:00",
                    "2020-01-01 00:01:00",
                    "2020-01-02 00:01:00",
                ],
            }
        )

        proc = pp.AsType({"a": "int64", "b": "datetime"})
        (df,) = proc.process([df])

        xdf = df.copy()
        xdf.a = xdf.a.astype("int64")
        xdf.b = pd.to_datetime(xdf.b)
        assert_frame_equal(df, xdf)
