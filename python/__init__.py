import logging
import importlib

from . import finder

logger = logging.getLogger(__name__)

def get_missions():
    importlib.reload(finder)

    return finder.get_missions()
