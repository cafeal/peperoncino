from typing import List, Optional
import pandas as pd
from peperoncino import MergedProcessing


class AsCategory(MergedProcessing):
    """Change dtypes as category.

    Parameters
    ----------
    cols: List[str]
    fillna: Optional[str]
        If this is not None, missing values will be
        filled by this value and use it as category.
    """

    def __init__(self, cols: List[str], fillna: Optional[str] = None):
        super().__init__()
        self._cols = cols
        self._fillna = fillna

    def simul_process(self, df: pd.DataFrame) -> pd.DataFrame:
        if self._fillna is not None:
            cols = df.get(self._cols)
            cols = cols.fillna(self._fillna)
            df = df.assign(**cols.to_dict("siries"))

        df = df.astype({c: "category" for c in self._cols})

        return df
