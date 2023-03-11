from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.application.models_in import AuthModelIn
from app.helpers.get_logger import get_logger
from app.tmp_model.modeldev import Usuario
from app.domain.user import User as UsuarioEntity

logger = get_logger(__name__)


class UsersRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def _to_entity(self, usuario: Usuario) -> UsuarioEntity:
        return UsuarioEntity(
            id=usuario.id,
            username=usuario.username,
            password=usuario.password,
        )

    def auth(self, user: AuthModelIn) -> UsuarioEntity:
        """Retorna el usuario encontrado en la base de datos, si no lo encuentra retorna None"""

        logger.info("Verificando si existe un usuario con nombre %s", user.username)
        with self.session_factory() as session:
            resultado = (
                session.query(Usuario)
                .filter(Usuario.username == user.username, Usuario.password == user.password)
                .first()
            )

            if resultado is None:
                return None

            usuario = resultado
            return self._to_entity(usuario)

    def find(self, username: str) -> UsuarioEntity:
        logger.info("Verificando si existe un usuario con nombre %s", username)
        with self.session_factory() as session:
            resultado = session.query(Usuario).filter(Usuario.username == username).first()

            if resultado is None:
                return None

            usuario = resultado
            return self._to_entity(usuario)
