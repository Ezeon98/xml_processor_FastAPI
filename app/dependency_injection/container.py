"""Containers module."""

from dependency_injector import containers, providers
import os
from app.persistence.database import Database
from app.persistence.users_repository import UsersRepository
from app.application.auth_service import AuthService
from app.application.read_service import ReadService
from app.application.fields_check_service import FieldCheckService
from app.application.add_fields_service import AddFieldService

from app.application.fields_filter_service import FieldFilterService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app.api.v1.router"])

    # DATABASE

    pg_host = os.getenv("PG_HOST")
    pg_port = os.getenv("PG_PORT")
    pg_db = os.getenv("PG_DB")
    pg_user = os.getenv("PG_USER")
    pg_password = os.getenv("PG_PASSWORD")

    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{pg_user}:{pg_password}@{pg_host}:{int(pg_port)}/{pg_db}"
    )

    db = providers.Singleton(Database, db_url=SQLALCHEMY_DATABASE_URL)
    db().create_database()

    # REPOSITORIES

    users_repository = providers.Factory(
        UsersRepository,
        session_factory=db.provided.session,
    )

    # SERVICES

    auth_service = providers.Factory(
        AuthService,
        users_repository=users_repository,
    )

    read_service = providers.Factory(ReadService, users_repository=users_repository)

    fields_check_service = providers.Factory(FieldCheckService, users_repository=users_repository)
    field_filter_service = providers.Factory(FieldFilterService, users_repository=users_repository)
    add_field_service = providers.Factory(AddFieldService, users_repository=users_repository)
