import pytest
import pandas as pd
import pupil as pp


class TestAsCategory:
    @pytest.mark.parametrize("fillna", [None, "NaN"])
    def test_process(self, fillna):
        df = pd.DataFrame(
            {
                "a": ["foo", None, "bar", None, "baz", None],
                "b": [None, "xxx", None, "yyy", None, "zzz"],
            }
        )
        proc = pp.AsCategory(["a"], fillna=fillna)

        (df,) = proc.process([df])
        assert isinstance(df.a.dtype, pd.CategoricalDtype)
        assert df.dtypes["b"] == "object"

        if fillna:
            assert set(df.a.cat.categories) == {"foo", "bar", "baz", "NaN"}
        else:
            assert set(df.a.cat.categories) == {"foo", "bar", "baz"}
