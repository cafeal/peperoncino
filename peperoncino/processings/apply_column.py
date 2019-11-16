from typing import Callable
import pandas as pd
from peperoncino import SeparatedProcessing


class ApplyColumn(SeparatedProcessing):
    """Apply function to a column.

    Parameters
    ----------
    col : str
    fn : Callable[[pd.Series], pd.Series]
        function to apply `col`.
    """

    def __init__(self, col: str, fn: Callable[[pd.Series], pd.Series]):
        super().__init__()
        self._col = col
        self._fn = fn

    def sep_process(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.assign(**{self._col: df[self._col].apply(self._fn)})
        return df
