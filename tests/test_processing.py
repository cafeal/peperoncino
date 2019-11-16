import pytest
import numpy as np
import pandas as pd
import peperoncino as pp


@pytest.fixture()
def df():
    # fmt: off
    return pd.DataFrame({
        'a': [1, 2, 3],
        'b': [4, 5, 6],
    })
    # fmt: on


class TestBaseProcessing:
    def test_processing(self, df):
        class Processing(pp.BaseProcessing):
            def _process(self, dfs):
                return [df + i for i, df in enumerate(dfs, 1)]

        proc = Processing()

        dfs = proc.process([df, df])

        assert len(dfs) == 2

        # fmt: off
        assert dfs[0].equals(pd.DataFrame({
            'a': [2, 3, 4],
            'b': [5, 6, 7],
        }))

        assert dfs[1].equals(pd.DataFrame({
            'a': [3, 4, 5],
            'b': [6, 7, 8],
        }))
        # fmt: on

    @pytest.mark.parametrize("is_fixed_columns", [True, False])
    def test_processing_columns_changes(self, df, is_fixed_columns):
        class Processing(pp.BaseProcessing):
            def _process(self, dfs):
                return [df.rename(columns={"a": "A"}) for i, df in enumerate(dfs, 1)]

        proc = Processing(is_fixed_columns=is_fixed_columns)

        if is_fixed_columns:
            with pytest.raises(pp.ColumnsChangedError):
                proc.process([df])
        else:
            (df,) = proc.process([df])
            assert (df.columns == ["A", "b"]).all()

    @pytest.mark.parametrize("is_fixed_rows", [True, False])
    def test_processing_rows_changes(self, df, is_fixed_rows):
        class Processing(pp.BaseProcessing):
            def _process(self, dfs):
                return [
                    pd.concat((df, df), ignore_index=True)
                    for i, df in enumerate(dfs, 1)
                ]

        proc = Processing(is_fixed_rows=is_fixed_rows)

        if is_fixed_rows:
            with pytest.raises(pp.RowsChangedError):
                proc.process([df])
        else:
            (_df,) = proc.process([df])
            assert len(_df) == len(df) * 2

    def test_only(self, df):
        class Processing(pp.BaseProcessing):
            def _process(self, dfs):
                return [df + i for i, df in enumerate(dfs, 1)]

        proc = Processing().only(0)

        dfs = proc.process([df, df])

        assert len(dfs) == 2

        # fmt: off
        assert dfs[0].equals(pd.DataFrame({
            'a': [2, 3, 4],
            'b': [5, 6, 7],
        }))

        assert dfs[1].equals(pd.DataFrame({
            'a': [1, 2, 3],
            'b': [4, 5, 6],
        }))
        # fmt: on


class ExampleSeparatedProcessing(pp.SeparatedProcessing):
    def sep_process(self, df):
        return df + 1


class TestSeparatedProcessing:
    def test_process(self, df):
        proc = ExampleSeparatedProcessing()

        dfs = proc.process([df, df])

        assert len(dfs) == 2

        # fmt: off
        assert dfs[0].equals(pd.DataFrame({
            'a': [2, 3, 4],
            'b': [5, 6, 7],
        }))

        assert dfs[1].equals(pd.DataFrame({
            'a': [2, 3, 4],
            'b': [5, 6, 7],
        }))
        # fmt: on


class ExampleMergedProcessing(pp.MergedProcessing):
    def __init__(self, dtype):
        super().__init__()
        self._dtype = dtype

    def simul_process(self, df):
        df.a = df.a + np.arange(len(df.a))
        df = df.astype({"a": self._dtype})
        return df


class TestMergedProcessing:
    @pytest.mark.parametrize(
        "dtype", ["float32", "float64", "int32", "int64", "Int32", "Int64"],
    )
    def test_process(self, df, dtype):
        proc = ExampleMergedProcessing(dtype)

        # fmt: off
        dfs = proc.process([
            df.assign(c=np.array([7, 8, 9])).astype(dtype),
            df.assign(d=np.array([10, 11, 12])).astype(dtype),
        ])
        # fmt: on

        assert len(dfs) == 2
        # fmt: off
        assert dfs[0].equals(pd.DataFrame({
            "a": [1, 3, 5],  # [1, 2, 3] + [0, 1, 2]
            "b": [4, 5, 6],
            "c": [7, 8, 9],
        }).astype(dtype))
        # fmt: on

        # fmt: off
        assert dfs[1].equals(pd.DataFrame({
            "a": [4, 6, 8],  # [1, 2, 3] + [3, 4, 5]
            "b": [4, 5, 6],
            "d": [10, 11, 12],
        }).astype(dtype))
        # fmt: on
