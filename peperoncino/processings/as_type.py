from typing import Dict
import pandas as pd
from peperoncino import SeparatedProcessing


class AsType(SeparatedProcessing):
    """Change dtypes.

    Parameters
    ----------
    mapping: Dict[str, str]
        Column - DType mapping.
    """

    def __init__(self, mapping: Dict[str, str]):
        super().__init__()

        _mapping = mapping.copy()
        _dt_cols = []
        for k in mapping:
            if mapping[k] == "datetime":
                _dt_cols.append(k)
                _mapping.pop(k)
            
        self._mapping = _mapping
        self._dt_cols = _dt_cols

    def sep_process(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.astype(self._mapping)

        df = df.assign(**{
            k: pd.to_datetime(df[k])
            for k in self._dt_cols
        })
        return df
