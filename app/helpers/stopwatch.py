"""Modulo helper para cronometrar funciones"""

import logging
from timeit import default_timer as timer

from app.helpers.get_logger import get_logger

_logger = get_logger(__name__)


def stopwatch(message="Tiempo de ejecucion: %s ms"):
    """Decorador que logea a debug el tiempo de ejecucion de una funcion"""

    def time_wrapper(func):
        def time(*args, **kwargs):
            try:
                start = timer()
                return func(*args, **kwargs)
            finally:
                end = timer()
                _logger.debug(message, (end - start) * 1000)

        return time

    return time_wrapper


class Stopwatch:
    """Context manager para cronometrar código"""

    def __init__(self, message="Tiempo de ejecucion: %s ms", level=logging.DEBUG) -> None:
        self._message_template = message
        self._start = None
        self._end = None
        self._level = level

    def __enter__(self):
        self._start = timer()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._end = timer()
        _logger.log(self._level, self._message_template, (self._end - self._start) * 1000)
        del exc_type
        del exc_val
        del exc_tb
