from functools import partial
from itertools import permutations
from itertools import product
from itertools import combinations
from itertools import combinations_with_replacement
from typing import List
import pandas as pd

from peperoncino import SeparatedProcessing


class Combinations(SeparatedProcessing):
    """Calculate combination features from pairs of columns.
    The name of calculated features are discribed as Reverse Polish Notation.

    Parameters
    ----------
    cols : List[str]
        Columns to be used for combination calculation.
    ops : List[str]
        Calculation operations. e.g. ops=['*', '/']
    comb_type : str
        How to calculate combination features.
        Available options are:
        - combinaions
        - combinations_with_replacement
        - product
        - permutaions
        Please refer to `itertools` for more details.
    """

    def __init__(
        self,
        cols: List[str],
        ops: List[str],
        comb_type: str = "combinations_with_replacement",
    ):
        super().__init__(is_fixed_columns=False)
        self._cols = cols
        self._ops = ops

        if comb_type == "combinations":
            self._comb_fn = partial(combinations, r=2)
        elif comb_type == "combinations_with_replacement":
            self._comb_fn = partial(combinations_with_replacement, r=2)
        elif comb_type == "product":
            self._comb_fn = partial(product, repeat=2)
        elif comb_type == "permutations":
            self._comb_fn = partial(permutations, r=2)
        else:
            raise ValueError(
                "`comb_type` should be one of"
                " 'combinations', 'combinatinos_with_replacement',"
                " 'product' and 'permutations'"
            )

    def sep_process(self, df: pd.DataFrame) -> pd.DataFrame:
        formulae = {}
        for a, b in self._comb_fn(self._cols):
            for op in self._ops:
                formulae[f"{op}_{a}_{b}"] = df.eval(f"{a} {op} {b}")
        return df.assign(**formulae)
