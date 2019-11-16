from typing import List
import pandas as pd
from peperoncino import BaseProcessing


class StatsEncoding(BaseProcessing):
    """Encoding columns by statistical values of target column.

    Parameters
    ----------
    cols : List[str]
        A list of column names to be encoded.
    target : str
        The name of the target column.
    ops : List[str]
        A list of aggregation operation function names (e.g. ['mean', 'std']).
    ref : int
        A reference dataframe index to calculate the mapping from categories
        to encodings.
        Default values is 0(first dataframe).
    """

    def __init__(
        self, cols: List[str], target: str, ops: List[str], ref: int = 0,
    ):
        super().__init__(is_fixed_columns=False)
        self._cols = cols
        self._target = target
        self._ops = ops
        self._ref = ref

    def _process(self, dfs: List[pd.DataFrame]) -> List[pd.DataFrame]:
        ref_df = dfs[self._ref]

        mapping = ref_df.groupby(self._cols)[self._target].agg(self._ops).reset_index()
        mapping = self._rename_op2col(mapping)

        dfs = [self._apply_mapping(df, mapping) for df in dfs]

        return dfs

    def _enc_names(self) -> List[str]:
        col_names = "&".join(self._cols)
        return [f"STATS_ENC_{col_names}_BY_{op}_{self._target}" for op in self._ops]

    def _rename_op2col(self, mapping: pd.DataFrame) -> pd.DataFrame:
        op2col = {op: name for op, name in zip(self._ops, self._enc_names())}
        return mapping.rename(columns=op2col)

    def _apply_mapping(self, df: pd.DataFrame, mapping: pd.DataFrame) -> pd.DataFrame:
        index = df.index

        # broadcast mapping to each row
        df = df.merge(
            mapping, on=self._cols, how="left", validate="many_to_one", sort=False,
        )
        df.index = index

        return df
