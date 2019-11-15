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
        assert pd.api.types.is_categorical_dtype(df.a)
        assert pd.api.types.is_string_dtype(df.b)

        if fillna:
            assert set(df.a.cat.categories) == {"foo", "bar", "baz", "NaN"}
        else:
            assert set(df.a.cat.categories) == {"foo", "bar", "baz"}
