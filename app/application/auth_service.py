from app.application.models_in import AuthModelIn
from app.persistence.users_repository import UsersRepository


class AuthService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    def auth(self, model: AuthModelIn):
        return self.users_repository.auth(model)
