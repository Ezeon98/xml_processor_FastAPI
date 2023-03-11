"""Modulo con constantes"""
from app.application.responses import ResponseTypes

# =====EXAMPLES=====
FIELDS = [
    "rutemisor",
    "rznsoc",
    "fchemis",
    "mnt",
    "mnttotal",
    "tasaiva",
    "iva",
    "folio",
    "tipodte",
    "rutrecep",
    "folioref",
    "montoimp",
    "mntexe",
]
L_STRIP = ["{http://www.sii.cl/SiiDte", "3.org/2000/09/xmldsig#", "}"]

ALLOWED_XLS_FILES = ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]

STATUS_CODES = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.PARAMETERS_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
}

EXCLUDE_OF_ADD_FIELDS = ["Vías pago Alimentos", "Vías pago Bebidas"]
