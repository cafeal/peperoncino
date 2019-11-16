from typing import List
import pandas as pd
from pupil import BaseProcessing


def _broadcast_stats(stats: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    """Broadcast aggregated statistical values to dataframe rows.

    Parameters
    ----------
    stats : pd.DataFrame
        dataframe generated by df.groupby(columns).agg(agg_list)
    df : pd.DataFrame
        original dataframe

    Returns
    -------
    pd.DataFrame
        Broadcasted stats
    """

    cols = list(stats.index.names)
    stats = (
        stats.reset_index()
        .merge(df[cols], on=cols, how="right", validate="one_to_many")
        .drop(columns=cols)
    )
    stats.index = df.index
    return stats


class TargetEncoding(BaseProcessing):
    """Target Mean Encoding with smoothing.
    https://dl.acm.org/citation.cfm?id=507538

    Parameters
    ----------
    cols : List[str]
        Columns to be encoded.
    target : str
        The target column.
    ref : int
        Reference dataframe index. Default is 0.
    prior_weight : float
        Prior weight for smoothing.
        If `prior_weight` > 0.0, the encoded values are calculated as
        `n_i / (n_i+prior_weight) * mean_i + prior_weight / (n+prior_weight) * prior`,
        where n_i is number of rows for category[i] and prior is mean of values.
        Default is 1.0.
    impute_prior : bool
        If True, categories which is not appeared in reference dataframe
        will be imputed by prior(the average of target).
        Default is True.
    """

    def __init__(
        self,
        cols: List[str],
        target: str,
        ref: int = 0,
        prior_weight: float = 1.0,
        impute_by_prior: bool = True,
    ):
        super().__init__(is_fixed_columns=False)
        self._cols = cols
        self._target = target
        self._ref = ref
        self._prior_weight = prior_weight
        self._impute_by_prior = impute_by_prior

    @property
    def enc_name(self) -> str:
        col_names = "&".join(self._cols)
        return f"TARGET_ENC_{col_names}_BY_{self._target}"

    def _process(self, dfs: List[pd.DataFrame]) -> List[pd.DataFrame]:
        ref_df = dfs[self._ref]

        # mapping
        mapping = ref_df.groupby(self._cols)[self._target].agg(["count", "mean"])

        # smoothing
        global_prior = ref_df[self._target].mean()

        if self._prior_weight > 0.0:
            prior = mapping.assign(count=len(ref_df), mean=global_prior)
            lamb = mapping["count"] / (mapping["count"] + self._prior_weight)
            mapping["mean"] = lamb * mapping["mean"] + (1 - lamb) * prior["mean"]

        mapping = mapping[["mean"]]
        dfs = [self._apply_mapping(df, mapping) for df in dfs]

        if self._impute_by_prior:
            dfs = [df.fillna({self.enc_name: global_prior}) for df in dfs]

        return dfs

    def _apply_mapping(self, df: pd.DataFrame, mapping: pd.DataFrame) -> pd.DataFrame:
        mapping = _broadcast_stats(mapping, df)

        # rename
        mapping = mapping.rename(columns={"mean": self.enc_name})

        df = df.merge(
            mapping,
            how="inner",
            left_index=True,
            right_index=True,
            sort=False,
            validate="one_to_one",
        )

        return df
