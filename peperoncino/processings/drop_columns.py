from typing import List
import pandas as pd
from peperoncino import SeparatedProcessing


class DropColumns(SeparatedProcessing):
    """Drop columns.

    Parameters
    ----------
    cols : List[str]
    """

    def __init__(self, cols: List[str]):
        super().__init__(is_fixed_columns=False)
        self._cols = cols

    def sep_process(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop(columns=self._cols)
