"""Módulo para instanciar loggers"""
import logging
import logging.config
import os
from pathlib import Path

import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

LOG_DEFAULT_LEVEL = os.getenv("LOG_DEFAULT_LEVEL", "INFO")
LOG_CONFIG_PATH = os.getenv("LOG_CONFIG_PATH", "./logging.ini")
LOG_PATH = os.getenv("LOG_PATH", "./logs/log.log")
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s | %(levelname)s | %(name)s :: %(message)s")
LOG_DATE_FORMAT = os.getenv("LOG_DATE_FORMAT", "%d/%m/%Y %H:%M:%S")


class ColorFormatter(logging.Formatter):
    """Clase de formatter para logs a consola"""

    def __init__(self, fmt=..., datefmt=..., style="%", validate=...) -> None:
        super().__init__(fmt, datefmt, style, validate)
        # Cachear diccionario de formatters
        self._color_formatters = {
            logging.DEBUG: logging.Formatter(self._fmt),
            logging.INFO: logging.Formatter(Fore.GREEN + self._fmt + Fore.RESET),
            logging.WARNING: logging.Formatter(Fore.YELLOW + self._fmt + Fore.RESET),
            logging.ERROR: logging.Formatter(Fore.RED + self._fmt + Fore.RESET),
            logging.CRITICAL: logging.Formatter(
                Fore.RED + Style.BRIGHT + self._fmt + Style.RESET_ALL + Fore.RESET
            ),
        }

    def format(self, record: logging.LogRecord) -> str:
        """Formatear con color según el diccionario de formatters a color cacheados y el nivel"""
        return self._color_formatters[record.levelno].format(record)


def get_logger(name: str, level=LOG_DEFAULT_LEVEL):
    """Retorna una nueva instancia de logger ya configurada"""
    Path(LOG_PATH).resolve().parent.mkdir(exist_ok=True, parents=True)
    new_logger = logging.getLogger(name)
    new_logger.setLevel(level)
    # Limpiar handlers en caso de que el logger ya haya estado inicializado
    new_logger.handlers = []

    color_formatter = ColorFormatter(LOG_FORMAT, LOG_DATE_FORMAT)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(color_formatter)

    formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    file_handler.setFormatter(formatter)

    new_logger.addHandler(stream_handler)
    new_logger.addHandler(file_handler)

    return new_logger


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    logger = get_logger(__name__)
    # Si no se limpian los handlers este mensaje se produce dos veces
    logger.info("second logger info message")
