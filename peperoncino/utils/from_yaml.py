import yaml
import peperoncino as pp


def from_yaml(yml_string: str) -> pp.Pipeline:
    """Create pipeline from yaml.
    `dict` corresponds to a processing
    and `list` of `dict` corresponds to a pipeline.

    ```
    yml = '''
    processing:
        -   name: Query
            query: "foo > 0"
        -   name: DropColumns
            cols:
                - foo
    '''

    pipeline = pp.from_yaml(yml)

    # `pipeline` equals to
    #
    # pp.Pipeline(
    #     pp.Query("foo > 0")
    #     pp.DropColumns(["foo"])
    # )
    ```

    Parameters
    ----------
    yml_string : str
        YAML string.
        This must include `processing` key.
        `name` key specifies processing class name
        and other keys are passed to it as arguments.

    Returns
    -------
    pp.Pipeline
    """

    yml = yaml.load(yml_string)
    pipeline = pp.from_list(yml["processing"])
    return pipeline
