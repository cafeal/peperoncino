import peperoncino as pp


def test_from_list():
    proc_list = [
        [
            {"name": "Query", "query": "foo > 0"},
            {"name": "DropColumns", "cols": ["foo", "bar"]},
        ],
        [{"name": "Select", "cols": ["baz"]}],
    ]
    pipeline = pp.from_list(proc_list)

    assert isinstance(pipeline.procs[0], pp.Pipeline)
    assert isinstance(pipeline.procs[0].procs[0], pp.Query)
    assert isinstance(pipeline.procs[0].procs[1], pp.DropColumns)
    assert isinstance(pipeline.procs[1], pp.Pipeline)
    assert isinstance(pipeline.procs[1].procs[0], pp.Select)
