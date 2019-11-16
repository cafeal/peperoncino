from typing import List
import pandas as pd
from peperoncino import SeparatedProcessing


class Select(SeparatedProcessing):
    def __init__(self, cols: List[str], lackable_cols: List[str] = []):
        super().__init__(is_fixed_columns=False)
        self._cols = cols
        self._lackable_cols = lackable_cols

    def sep_process(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = self._cols
        df_cols = df.columns.tolist()

        for c in self._cols:
            if c not in df.columns and c not in self._lackable_cols:
                raise ValueError(f"Column {c} must not be lacked.")

        cols = [c for c in cols if c in df_cols]
        return df[cols]
