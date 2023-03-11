"""Módulo de helpers de fechas y horas"""

from datetime import datetime
from dateutil import tz, parser

from app.domain.constants import API_DATETIME_FORMAT

tz_local = tz.tzoffset("GTM-3", -1 * 3 * 60 * 60)  # offset en segundos = horas * minutos * segundos


def datetime_from_string(date_str: str) -> datetime:
    """Parsea una fecha según un string con el formato de la API"""
    if isinstance(date_str, str):
        _datetime = parser.isoparse(date_str)
        _datetime_tz = _datetime.astimezone(tz_local)
        _datetime_tz = _datetime_tz.replace(tzinfo=None)
        return _datetime_tz
    return date_str


def get_period(periodo_date: datetime, period_format="%Y%m") -> str:
    """Retorna el periodo de la fecha ingresada"""
    return periodo_date.strftime(period_format)
