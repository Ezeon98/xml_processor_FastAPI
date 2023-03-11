from app.helpers.get_logger import get_logger
import pandas as pd
import json
from app.domain.constants import ALLOWED_XLS_FILES

logger = get_logger(__name__)


def dedouble_values(dic):
    try:
        new_dict = {}
        for key, valores in dic.items():
            for i, valor in enumerate(valores):
                new_key = "{}_{}".format(key, i)
                if new_key in new_dict:
                    new_dict[new_key].append(valor)
                else:
                    new_dict[new_key] = [valor]
            if len(valores) == 1 and key not in new_dict:
                new_dict["{}_{}".format(key, 0)] = valores
        return new_dict
    except Exception:
        logger.exception("Error al Desdoblar el Diccionario")


def read_xlsx(file, skip, sheet):
    try:
        df = pd.read_excel(file, skiprows=skip, sheet_name=sheet)
        df = json.loads(df.to_json(orient="records"))
        return df
    except Exception:
        logger.exception("Error al Leer el xlsx. Compruebe el numero Skip y Sheet")


def check_type_files(xlsx_file):
    try:
        if xlsx_file.content_type not in ALLOWED_XLS_FILES:
            return False
        return True
    except Exception:
        logger.exception("Error al hacer el check_type_files")
