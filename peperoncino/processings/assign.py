from typing import Any
import pandas as pd
from peperoncino import SeparatedProcessing


class Assign(SeparatedProcessing):
    """Assign values to dataframes by given formula.
    scalar values are also applicable.

    e.g.
    ```
    import pp
    pp.Assign(
        foo = 'xxx * yyy',
        bar = 1,
    )
    ```

    Parameters
    ----------
    **formula : Any
        formula or values
    """

    def __init__(self, **formula: Any):
        super().__init__(is_fixed_columns=False)
        self._formula = formula

    def sep_process(self, df: pd.DataFrame) -> pd.DataFrame:
        _assign = {}
        for k, f in self._formula.items():
            if isinstance(f, str):
                val = df.eval(f)
            else:
                val = f
            _assign[k] = val
        df = df.assign(**_assign)
        return df
