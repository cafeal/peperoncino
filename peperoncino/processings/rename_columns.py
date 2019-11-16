from typing import Dict
import pandas as pd
from peperoncino import SeparatedProcessing


class RenameColumns(SeparatedProcessing):
    """Rename columns.

    Parameters
    ----------
    mapping: Dict[str, str]
        The name mapping.
    **kwargs:
        Keyward arguments are also concerned as the mapping.
    """

    def __init__(self, mapping: Dict[str, str] = {}, **kwargs: str):
        super().__init__(is_fixed_columns=False)
        mapping.update(kwargs)
        self._mapping = mapping

    def sep_process(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(self._mapping, axis=1)
