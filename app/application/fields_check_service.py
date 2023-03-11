from app.persistence.users_repository import UsersRepository
from app.application.custom_exceptions import ParameterException
from app.application.responses import ResponseFailure, ResponseTypes
from app.helpers.get_logger import get_logger
import json
from app.domain.utils import read_xlsx

logger = get_logger(__name__)


class FieldCheckService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    def fields_check(self, xlsx_file, json_file, rows, sheet, columns):
        json_dict = json.loads(json_file)
        xlsx_dict = read_xlsx(xlsx_file, rows, sheet)

        try:
            for dic in json_dict:
                if dic["name"] == columns.json_column:
                    valid = dic["value"] in str([dic2[columns.xlsx_column] for dic2 in xlsx_dict])
                    if valid:
                        return json_dict
                    else:
                        dic["valid"] = False
                        json_dict[0]["valid"] = False
                        if json_dict[0]["value"] == "":
                            json_dict[0]["value"] = json_dict[0]["value"] + dic["name"]
                        else:
                            json_dict[0]["value"] = json_dict[0]["value"] + ", " + dic["name"]
                        return json_dict
            return ResponseFailure(
                ResponseTypes.PARAMETERS_ERROR, "No se encuentra la key enviada en el JSON"
            )
        except Exception:
            return ResponseFailure(
                ResponseTypes.PARAMETERS_ERROR,
                "Chequee los parametros rows,sheet y xlsx_column",
            )
