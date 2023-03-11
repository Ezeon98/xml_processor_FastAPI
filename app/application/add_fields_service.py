from app.persistence.users_repository import UsersRepository
from app.application.custom_exceptions import ParameterException
from app.application.responses import ResponseFailure, ResponseTypes
from app.helpers.get_logger import get_logger
import json
from app.domain.utils import read_xlsx
import pandas as pd
import ast
from app.domain.constants import EXCLUDE_OF_ADD_FIELDS

logger = get_logger(__name__)


class AddFieldService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    def add_fields(self, xlsx_file, json_data, info):
        final_data = ""
        data = []
        result = []
        json_dict = ast.literal_eval(json_data)

        xlsx_df = pd.DataFrame(read_xlsx(xlsx_file, info.rows, info.sheet))

        try:
            xlsx_df[info.column_to_compare] = xlsx_df[info.column_to_compare].astype(str)
        except KeyError:
            return ResponseFailure(
                ResponseTypes.PARAMETERS_ERROR,
                f"No se encuentra la columna {info.column_to_compare}",
            )

        try:
            xlsx_df[info.column_to_find] = xlsx_df[info.column_to_find].astype(str)
        except KeyError:
            return ResponseFailure(
                ResponseTypes.PARAMETERS_ERROR, f"No se encuentra la columna {info.column_to_find}"
            )
        for i in range(0, xlsx_df.shape[0]):
            try:
                value = xlsx_df.loc[
                    xlsx_df[info.column_to_compare] == (json_dict[info.pos]["value"]),
                    info.column_to_find,
                ].values[i]
                data.append(value)
                if value == "None":
                    data = list(filter(lambda x: x != "None", data))
                    break
            except Exception:
                break
        if len(data) != 0:
            final_data = ";".join(data)
            final_data = final_data.replace("None;", "")
        new_value = {"name": info.column_to_find, "value": final_data, "valid": True}
        result.append(new_value)
        return result
