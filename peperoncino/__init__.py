__version__ = "0.0.5"

from peperoncino.processing import BaseProcessing  # NOQA
from peperoncino.processing import SeparatedProcessing  # NOQA
from peperoncino.processing import MergedProcessing  # NOQA
from peperoncino.processing import ColumnsChangedError  # NOQA
from peperoncino.processing import RowsChangedError  # NOQA

from peperoncino.processings.pipeline import Pipeline  # NOQA
from peperoncino.processings.query import Query  # NOQA
from peperoncino.processings.apply_column import ApplyColumn  # NOQA
from peperoncino.processings.as_type import AsType  # NOQA
from peperoncino.processings.as_category import AsCategory  # NOQA
from peperoncino.processings.rename_columns import RenameColumns  # NOQA
from peperoncino.processings.assign import Assign  # NOQA
from peperoncino.processings.drop_columns import DropColumns  # NOQA
from peperoncino.processings.drop_duplicates import DropDuplicates  # NOQA
from peperoncino.processings.combinations import Combinations  # NOQA
from peperoncino.processings.select import Select  # NOQA
from peperoncino.processings.stats_encoding import StatsEncoding  # NOQA
from peperoncino.processings.target_encoding import TargetEncoding  # NOQA

from peperoncino.utils.from_list import from_list  # NOQA
from peperoncino.utils.from_yaml import from_yaml  # NOQA


def get_logger():  # type: ignore
    import logging
    import sys

    logger = logging.getLogger("peperoncino")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(levelname)s]\tpeperoncino:\t%(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


logger = get_logger()
