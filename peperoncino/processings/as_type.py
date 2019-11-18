from typing import Dict
import pandas as pd
from peperoncino import SeparatedProcessing


class AsType(SeparatedProcessing):
    """Change dtypes.

    Parameters
    ----------
    mapping: Dict[str, ]
    """

    def __init__(self, mapping: Dict[str, str]):
        super().__init__()
        self._mapping = mapping

    def sep_process(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.astype(self._mapping)
        return df
