from pydantic import BaseModel, constr


class AuthModelIn(BaseModel):
    """AuthModelIn"""

    username: constr(min_length=1, max_length=50)
    password: constr(min_length=1, max_length=50)


class Columns(BaseModel):
    """Columns In"""

    xlsx_column: str
    json_column: str


class AddFields(BaseModel):
    pos: int = 0
    column_to_compare: str = "RUT / CUIT"
    column_to_find: str = "Acreedor/Vendor"
    rows: int = 4
    sheet: int = 0
