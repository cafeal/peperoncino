import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import pupil as pp


class TestAssign:
    def test_process(self):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        proc = pp.Assign(c="a * b", d=1, e=np.nan)
        (df,) = proc.process([df])
        assert_frame_equal(
            df,
            pd.DataFrame(
                {
                    "a": [1, 2, 3],
                    "b": [4, 5, 6],
                    "c": [4, 10, 18],  # [1, 2, 3] x [4, 5, 6]
                    "d": [1, 1, 1],
                    "e": [np.nan, np.nan, np.nan],
                }
            ),
        )
