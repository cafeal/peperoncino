from typing import List, Optional
import pandas as pd
from peperoncino import SeparatedProcessing


class DropDuplicates(SeparatedProcessing):
    """Drop duplicate rows.

    Parameters
    ----------
    cols : Optinal[List[str]]
        Only these columns are considered for uniqueness
        If this is None, all columns are considered.
        Default value is `None`.
    """

    def __init__(self, cols: Optional[List[str]] = None):
        super().__init__(is_fixed_rows=False)
        self._cols = cols

    def sep_process(self, df: pd.DataFrame) -> pd.DataFrame:
        _df = df
        if self._cols is not None:
            _df = df.get(self._cols)
        index = _df.drop_duplicates().index
        return df.loc[index]
