from __future__ import annotations
from abc import ABCMeta
from abc import abstractmethod
from typing import List, Union, Any, Optional
import pandas as pd

import pupil as pp


class ColumnsChangedError(Exception):
    pass


class RowsChangedError(Exception):
    pass


class BaseProcessing(metaclass=ABCMeta):
    """
    Abstruct class for data processing
    """

    def __init__(self, is_fixed_columns: bool = True, is_fixed_rows: bool = True):
        self._is_fixed_columns = is_fixed_columns
        self._is_fixed_rows = is_fixed_rows
        self._logs: List[Any] = []
        self._indices: Optional[List[int]] = None

    @property
    def is_fixed_columns(self) -> bool:
        return self._is_fixed_columns

    @property
    def is_fixed_rows(self) -> bool:
        return self._is_fixed_rows

    def _logging(self, msg: str, level: str = "info") -> None:
        if level not in ["fatal", "error", "warning", "info", "debug"]:
            raise ValueError(
                "`level` should be one of fatal, error, warning, info and debug"
            )
        self._logs.append((msg, level))

    def _flush_logs(self) -> None:
        for msg, level in self._logs:
            log_fn = getattr(pp.logger, level)
            log_fn(msg)
        self._logs.clear()

    def process(self, dfs: List[pd.DataFrame]) -> List[pd.DataFrame]:
        """Processing dataframes

        Parameters
        ----------
        dfs : List[pd.DataFrame]

        Returns
        -------
        List[pd.DataFrame]
        """

        self._logging(f"Applying: {self.__class__.__name__}")

        # memory columns
        orig_cols = [df.columns for df in dfs]
        orig_rows = [df.index for df in dfs]

        dfs = self._process_with_limitation(dfs)

        cols = [df.columns for df in dfs]
        rows = [df.index for df in dfs]

        self._logging_summary(cols, rows, orig_cols, orig_rows)
        self._flush_logs()

        for i, (col, orig_col) in enumerate(zip(cols, orig_cols)):
            col, orig_col = set(col), set(orig_col)
            if self.is_fixed_columns and len(col | orig_col) != len(col & orig_col):
                raise ColumnsChangedError(
                    f"Number of columns are changed in df[{i}]."
                    f"Please refer to logs by setting proc.set_log_level(logging.DEBUG)"
                )

        for i, (row, orig_row) in enumerate(zip(rows, orig_rows)):
            if self.is_fixed_rows and len(row | orig_row) != len(row & orig_row):
                raise RowsChangedError(
                    f"Number of rows are changed in df[{i}]."
                    f"Please refer to logs by setting proc.set_log_level(logging.DEBUG)"
                )

        return dfs

    @abstractmethod
    def _process(self, dfs: List[pd.DataFrame]) -> List[pd.DataFrame]:
        """Abstract method of processing

        Parameters
        ----------
        dfs : List[pd.DataFrame]

        Returns
        -------
        List[pd.DataFrame]
        """
        pass

    def _process_with_limitation(self, dfs: List[pd.DataFrame]) -> List[pd.DataFrame]:
        # limit dataframes by `only` function
        indices = self._indices
        if indices is None:
            indices = list(range(len(dfs)))

        _dfs = [df for i, df in enumerate(dfs) if i in indices]
        _dfs = self._process(_dfs)

        for i in range(len(dfs)):
            if i in indices:
                dfs[i] = _dfs.pop(0)

        return dfs

    def _logging_summary(
        self,
        cols: List[pd.Index],
        rows: List[pd.Index],
        orig_cols: List[pd.Index],
        orig_rows: List[pd.Index],
    ) -> None:
        for i, (col, row, orig_col, orig_row) in enumerate(
            zip(cols, rows, orig_cols, orig_rows)
        ):
            added_cols = set(col) - set(orig_col)
            dropped_cols = set(orig_col) - set(col)

            self._logging(f"df[{i}]")
            self._logging(f"#cols: {len(orig_col)} ---> {len(col)}")
            self._logging(f"+cols: {added_cols}", level="debug")
            self._logging(f"-cols: {dropped_cols}", level="debug")
            self._logging(f"#rows: {len(orig_row)} ---> {len(row)}")

    def only(self, indices: Union[int, List[int]]) -> BaseProcessing:
        """Limit the scope of processing

        Parameters
        ----------
        indices : Union[int, List[int]]

        Returns
        -------
        BaseProcessing
            self
        """

        if not isinstance(indices, int) or isinstance(indices, list):
            raise ValueError("indices must be int or list of ints")

        if isinstance(indices, int):
            indices = [indices]

        self._indices = indices
        return self


class SeparatedProcessing(BaseProcessing):
    """
    Abstract class to process each dataframe separatedly.
    """

    def _process(self, dfs: List[pd.DataFrame]) -> List[pd.DataFrame]:
        return [self.sep_process(df) for df in dfs]

    @abstractmethod
    def sep_process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processing for single dataframe.

        Parameters
        ----------
        df : pd.DataFrame

        Returns
        -------
        pd.DataFrame
            A processed dataframe.
        """
        pass


class MergedProcessing(BaseProcessing):
    """
    Merge all dataframe and apply some processing simultaniously.
    """

    def _process(self, dfs: List[pd.DataFrame]) -> List[pd.DataFrame]:
        dtypes = [df.dtypes for df in dfs]
        dfs = [df.assign(__DFID__=i) for i, df in enumerate(dfs)]
        merged_df = pd.concat(dfs, axis=0, sort=False)

        original_index = merged_df.index
        merged_df = merged_df.reset_index(drop=True)

        dropped_cols = []
        for df in dfs:
            # columns by merging will be dropped
            dropped_cols.append(set(merged_df.columns) - set(df.columns))

        merged_df = self.simul_process(merged_df)
        merged_df.index = original_index

        for i, (df, dtype) in enumerate(zip(dfs, dtypes)):
            # columns dropped in processing will be dropped too
            dcols = set(df.columns) - set(merged_df.columns)
            dcols |= dropped_cols[i]
            cols = [c for c in merged_df.columns if c not in dcols]

            df = merged_df.query("__DFID__ == @i").get(cols)
            df = df.drop(columns="__DFID__")
            dfs[i] = df.astype(dtype)

        return dfs

    @abstractmethod
    def simul_process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processing for the merged dataframe

        Parameters
        ----------
        df : pd.DataFrame

        Returns
        -------
        pd.DataFrame
        """
        pass
