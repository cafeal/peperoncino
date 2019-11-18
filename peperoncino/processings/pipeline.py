from typing import List, Tuple
import pandas as pd
from peperoncino import BaseProcessing


class Pipeline(BaseProcessing):
    """Connect multiple processings

    Parameters
    ----------
    *procs : List[BaseProcessing]
    """

    def __init__(self, *procs: BaseProcessing):
        super().__init__(is_fixed_columns=False, is_fixed_rows=False)
        self._procs = procs

    @property
    def procs(self) -> Tuple[BaseProcessing, ...]:
        return self._procs

    def _process(self, dfs: List[pd.DataFrame]) -> List[pd.DataFrame]:
        for p in self._procs:
            dfs = p.process(dfs)
        return dfs
