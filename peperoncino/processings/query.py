import pandas as pd
from peperoncino import SeparatedProcessing


class Query(SeparatedProcessing):
    """Query records in dataframe.

    Parameters
    ----------
    query : str
        query strings to be passed to pd.DataFrame.query.
    """

    def __init__(self, query: str):
        super().__init__(is_fixed_rows=False)
        self._query = query

    def sep_process(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.query(self._query)
