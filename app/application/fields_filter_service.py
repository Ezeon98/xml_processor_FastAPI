from app.persistence.users_repository import UsersRepository
from app.application.custom_exceptions import ParameterException
from app.application.responses import ResponseFailure, ResponseTypes
from app.helpers.get_logger import get_logger
import os
import ast
import json
from app.helpers.field_filter_connector import FieldFilterConnector as dc


logger = get_logger(__name__)
url_api_datareader = os.getenv("BASE_URL_API_DATAREADER")
user_datareader = os.getenv("USER_API_DATAREADER")
pass_datareader = os.getenv("PASSWORD_API_DATAREADER")


class FieldFilterService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository
        self.field_filter = dc(url_api_datareader, logger)
        self.field_filter.auth(user_datareader, pass_datareader)

    def charge_db(self, field_name: str, field_value: list):
        loads = 0
        not_loads = 0
        stringfied_data = []
        field_value = json.loads(field_value)
        try:
            for d in field_value:
                new_dict = {}
                for key, value in d.items():
                    if isinstance(value, (int, float)):
                        new_dict[key] = str(value)
                    else:
                        new_dict[key] = value
                stringfied_data.append(new_dict)
        except Exception:
            raise Exception

        for dic in stringfied_data:
            if self.field_filter.charge_db(field_name, str(dic)):
                loads += 1
            else:
                not_loads += 1
        return f"Registros cargados: {loads}, Registros NO cargados: {not_loads}"

    def delete_field(self, field: str):
        return self.field_filter.remove_field_filters(field)

    def search_field(self, field_name: str, field_value: str, data: str):
        results = self.field_filter.search_fields(field_name, field_value)
        dict2 = ast.literal_eval(data)
        try:
            if results:
                for dic in results:
                    dict1 = eval(dic["field_value"])
                    for key, value in dict2.items():
                        if key not in dict1 or dict1[key] != value:
                            break
                    else:
                        return True
                else:
                    return False
        except Exception:
            raise Exception
