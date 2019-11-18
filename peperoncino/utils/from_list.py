from typing import List, Dict, Union, Any, cast
import peperoncino as pp


def from_list(proc_list: List[Dict[str, Any]]) -> pp.Pipeline:
    """Create pipeline from list.
    `dict` corresponds to a processing
    and `list` of `dict` corresponds to a pipeline.

    ```
    proc_list = [
        {"name": "Query", "query": "foo > 0"},
        {"name": "DropColumns", "cols": ["foo"]},
    ]

    pipeline = pp.from_list(proc_list)

    # this `pipeline` equals to
    # pp.Pipeline(
    #     pp.Query("foo > 0")
    #     pp.DropColumns(["foo"])
    # )
    ```

    Parameters
    ----------
    proc_list : List[Dict[str, Any]]
        List of dictionaries of processing attributes.
        `name` key specifies processing class
        and other keys are passed to it as arguments.
    
    Returns
    -------
    pp.Pipeline
        [description]
    """
    proc = _create_pipeline(proc_list)
    pipeline = cast(pp.Pipeline, proc)
    return pipeline


def _create_pipeline(
    proc: Union[Dict[str, str], List[Dict[str, Any]]]
) -> pp.BaseProcessing:
    if isinstance(proc, dict):
        return _resolve_proc(proc)

    elif isinstance(proc, list):
        return _resolve_pipeline(proc)
    else:
        raise ValueError()


def _resolve_pipeline(proc: List[Dict[str, Any]]) -> pp.Pipeline:
    procs = []
    for _p in proc:
        p = _create_pipeline(_p)
        procs.append(p)
    pipeline = pp.Pipeline(*procs)
    return pipeline


def _resolve_proc(proc_dict: Dict[str, Any]) -> pp.BaseProcessing:
    proc_name = proc_dict.pop("name")
    proc_class = _get_proc_by_name(proc_name)
    proc: pp.BaseProcessing = proc_class(**proc_dict)
    return proc


def _get_proc_by_name(name: str) -> type:
    proc: type = getattr(pp, name)
    return proc
