from app.persistence.users_repository import UsersRepository
from app.application.custom_exceptions import ParameterException
from app.application.responses import ResponseFailure, ResponseTypes
from app.helpers.get_logger import get_logger
import xml.etree.ElementTree as ET
import pandas as pd
import json

from app.domain.constants import L_STRIP
from app.domain.utils import dedouble_values

logger = get_logger(__name__)


class ReadService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    def read_xml(self, file, fields):
        try:
            keys = ["Valid"]
            values = [""]

            def get_root(file):
                root = ET.fromstring(file)
                return root

            def build_dict(root):
                for field in root.iter(root.tag):
                    tags = [elem.tag for elem in field.iter()]
                    text = [elem.text for elem in field.iter()]
                dic = {}
                for v, k in zip(text, tags):
                    if k not in dic.keys():
                        dic[k] = [v]  # creamos la clave si no existe
                    else:
                        dic[k].append(v)
                for i in L_STRIP:
                    dic = {key.lstrip(i): value for key, value in dic.items()}
                return dic

            def make_df(data):
                exists = 0
                for key, value in dic.items():
                    if key.startswith(data + "_"):
                        values.append(dic[key][0])
                        keys.append(key)
                        exists = 1
                    if key == data:
                        values.append(dic[data][0])
                        keys.append(data)
                        exists = 1
                if exists == 0:
                    values.append(None)
                    keys.append(data)
                    logger.info(f"La clave {data} no existe en el XML")

            root = get_root(file=file)

            dic = dedouble_values(build_dict(root))

            try:
                for i in fields:
                    make_df(i)
                logger.info("Extraccion de datos finalizada")
            except Exception:
                logger.error("Error al crear el DataFrame")

            dictionary = {"name": keys, "value": values, "valid": True}
            df = pd.DataFrame(dictionary)
            response = df.to_json(orient="records")

            return json.loads(response)

        except ParameterException as ex:
            return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, ex)
        except Exception as ex:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, ex)
