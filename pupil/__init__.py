__version__ = "0.1.0"

from pupil.processing import BaseProcessing  # NOQA
from pupil.processing import SeparatedProcessing  # NOQA
from pupil.processing import MergedProcessing  # NOQA
from pupil.processing import ColumnsChangedError  # NOQA
from pupil.processing import RowsChangedError  # NOQA

from pupil.processings.pipeline import Pipeline  # NOQA
from pupil.processings.query import Query  # NOQA
from pupil.processings.apply_column import ApplyColumn  # NOQA
from pupil.processings.as_category import AsCategory  # NOQA


def get_logger():  # type: ignore
    import logging
    import sys

    logger = logging.getLogger("pupil")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(levelname)s]\tpupil:\t%(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


logger = get_logger()
