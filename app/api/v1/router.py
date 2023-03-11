from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Body
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


from dependency_injector.wiring import inject, Provide

from datetime import timedelta
from typing import List, Optional, Dict
from app.application.read_service import ReadService
from app.application.fields_check_service import FieldCheckService
from app.application.fields_filter_service import FieldFilterService
from app.application.add_fields_service import AddFieldService


from app.helpers.get_logger import get_logger
from app.application.auth_service import AuthService
from app.application.models_in import AuthModelIn, Columns, AddFields
from app.dependency_injection.container import Container
from app.domain.utils import check_type_files

from app.domain.constants import FIELDS

logger = get_logger(__name__)


router = APIRouter(
    prefix="",
    tags=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/auth")
@inject
def authenticate(
    model: AuthModelIn,
    auth: AuthJWT = Depends(),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    """Autentica el usuario según nombre de usuario y contraseña, retornando
    los tokens de acceso y actualizacion.
    """

    user_from_database = auth_service.auth(model)
    if user_from_database is not None:
        access_token = auth.create_access_token(
            subject=user_from_database.username, expires_time=timedelta(1, 0, 0, 0, 0, 0, 0)
        )  # 1 día de vigencia
        refresh_token = auth.create_refresh_token(
            subject=user_from_database.username, expires_time=timedelta(30, 0, 0, 0, 0, 0, 0)
        )  # 30 dias de vigencia

        return {"access_token": access_token, "refresh_token": refresh_token}
    raise HTTPException(status_code=401, detail="Autenticación incorrecta.")


@router.post("/refreshtoken", dependencies=[Depends(HTTPBearer())])
def refresh(auth: AuthJWT = Depends()):
    """Genera un nuevo token de acceso a partir del token
    de actualizacion, marcandolo como no-nuevo,
    ya que en esta ruta no se verifica la contraseña.
    """
    auth.jwt_refresh_token_required()

    current_user = auth.get_jwt_subject()
    new_access_token = auth.create_access_token(
        subject=current_user, expires_time=timedelta(1, 0, 0, 0, 0, 0, 0)
    )
    return {"access_token": new_access_token}


@router.post("/read_file", dependencies=[Depends(HTTPBearer())])
@inject
async def recognize(
    filedata: UploadFile = File(...),
    fields: List[str] = Query(default=FIELDS, alias="xml_fields"),
    authorize: AuthJWT = Depends(),
    read_service: ReadService = Depends(Provide[Container.read_service]),
):
    """
    Read files
    """
    try:
        authorize.jwt_required()
        if filedata.content_type == "text/xml":
            response = read_service.read_xml(await filedata.read(), fields)
            return response
    except Exception:
        raise HTTPException(400, detail="Invalid document type")


@router.post("/fields_check", dependencies=[Depends(HTTPBearer())])
@inject
async def fields_check(
    file_xlsx: UploadFile = File(...),
    json_data: str = Body(...),
    columns: Columns = Depends(),
    rows: Optional[int] = 4,
    sheet: Optional[int] = 0,
    authorize: AuthJWT = Depends(),
    fields_check_service: FieldCheckService = Depends(Provide[Container.fields_check_service]),
):
    """
    Check the data on Json Files.
    """
    try:
        authorize.jwt_required()
        if check_type_files(file_xlsx):
            response = fields_check_service.fields_check(
                await file_xlsx.read(), json_data, rows, sheet, columns
            )
            return response
    except Exception:
        raise Exception()


@router.post("/add_fields", dependencies=[Depends(HTTPBearer())])
@inject
async def add_fields(
    file_xlsx: UploadFile = File(...),
    json_data: str = Body(...),
    excel_info: AddFields = Depends(),
    authorize: AuthJWT = Depends(),
    add_field_service: AddFieldService = Depends(Provide[Container.add_field_service]),
):
    """
    Retrieve info of Excels
    """
    try:
        authorize.jwt_required()
        if check_type_files(file_xlsx):
            response = add_field_service.add_fields(await file_xlsx.read(), json_data, excel_info)
            return response
    except Exception:
        raise Exception()


@router.post("/field_filter/charge_db", dependencies=[Depends(HTTPBearer())])
@inject
async def charge_db(
    column: str,
    data: str,
    authorize: AuthJWT = Depends(),
    field_filter_service: FieldFilterService = Depends(Provide[Container.field_filter_service]),
):
    """
    Load the DB for Field_filter
    """
    try:
        authorize.jwt_required()
        response = field_filter_service.charge_db(column, data)
        return response
    except Exception:
        raise HTTPException(400, detail="Error in authentication/Charge Db")


@router.post("/field_filter/delete_field", dependencies=[Depends(HTTPBearer())])
@inject
async def delete_field(
    field: str,
    authorize: AuthJWT = Depends(),
    field_filter_service: FieldFilterService = Depends(Provide[Container.field_filter_service]),
):
    """
    Delete fields in Db
    """
    try:
        authorize.jwt_required()
        response = field_filter_service.delete_field(field)
        return response
    except Exception:
        raise HTTPException(400, detail="Error in authenthication/Delete Fields")


@router.post("/field_filter/search", dependencies=[Depends(HTTPBearer())])
@inject
async def search_field(
    field_name: str,
    field_value: str,
    data: str,
    authorize: AuthJWT = Depends(),
    field_filter_service: FieldFilterService = Depends(Provide[Container.field_filter_service]),
):
    """
    Search fields in Db (Via Like)
    """
    try:
        authorize.jwt_required()
        response = field_filter_service.search_field(field_name, field_value, data)
        return response
    except Exception:
        raise HTTPException(400, detail="Invalid params")
