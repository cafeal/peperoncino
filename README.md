# peperoncino: A library for easy data processing for pandas

## Install

```
$ pip install peperoncino
```

## How to use

### Processing DataFrame
```python
import peperoncino as pp

pipeline = pp.Pipeline(
    # query data
    pp.Query("bar <= 3"),
    # assign new feature
    pp.Assign(hoge="foo * bar"),
    # generate combination feature
    pp.Combinations(["foo", "baz"], ["*", "/"]),
    # target encoding
    pp.TargetEncoding(["baz"], "y", ref=0),
    # select features
    pp.Select(
        ["hoge", "*_foo_baz", "TARGET_ENC_baz_BY_y", "y"],
        lackable_cols=["y"],
    )
)

# execute the processing
train_df, val_df, test_df = \
    pipeline.process([train_df, val_df, test_df])
```

### Predefined processings

| name | description |
| :--- | :---------- |
| `ApplyColumn` | Apply a function to a column. |
| `AsCategory` | Assign `category` dtype to columns. |
| `Assign` | Assign a feature by a formula. |
| `Combinations` | Create combination features. |
| `DropColumns` | Drop columns. |
| `DropDuplicates` | Drop duplicate rows. |
| `Pipeline` | Chain processings. |
| `Query` | Query rows by a given condition. |
| `RenameCOlumns` | Rename columns. |
| `Select` | Select columns. |
| `StatsEncoding` | Encode columns by statistical values of another column. |
| `TargetEncoding` | Target Encoding with smoothing. |

### Define processing
All processings are subclass of `pp.BaseProcessing`.  
All you need is define the `_process(self, dfs: List[pd.DataFrame]) -> List[pd.DataFrame]` function.

```python
class ExampleProcessing(pp.BaseProcessing):
    def _process(self, dfs: List[pd.DataFrame]) -> List[pd.DataFrame]:
        return [df + 1 for df in dfs]
```

If your processing doesn't depent on each other data frames, then use `pp.SeparatedProcessing`.

```python
class ExampleProcessing(pp.SeparatedProcessing):
    def sep_process(self, df: pd.DataFrame) -> pd.DataFrame:
        return df * 2
```

If you need to merge all dataframes and then apply your processing, use `pp.MergedProcessing`.

```python
class ExampleProcessing(pp.SeparatedProcessing):
    def simul_process(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.assign(col1_mean=df['col1'].mean())
```


