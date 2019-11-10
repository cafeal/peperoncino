__version__ = "0.1.0"

from pupil.processing import BaseProcessing
from pupil.processing import SeparatedProcessing
from pupil.processing import MergedProcessing
from pupil.processing import ColumnsChangedError
from pupil.processing import RowsChangedError


def get_logger():
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
