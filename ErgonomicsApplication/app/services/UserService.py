# app/services/UserService.py
from typing import Optional, Type
from app.repository.UserRepository import UserRepository
from app.database.models import User


class UserService:

    def is_login_exists(self, login: str) -> bool:
        with UserRepository() as repo:
            return repo.is_login_exists(login)

    def create_user(self, user_data: dict) -> int:
        with UserRepository() as repo:
            return repo.create_user(user_data)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        with UserRepository() as repo:
            return repo.get_user_by_id(user_id)

    def check_user(self, login: str, password: str) -> tuple[str, int] | None:
        """
        Возвращает (FIO, user_id), если логин и пароль правильные,
        иначе None.
        """
        with UserRepository() as repo:
            result = repo.check_user_with_id(login, password)
            if result:
                return result
            return None

    def update_user(self, user_id: int, update_data: dict) -> User:
        with UserRepository() as repo:
            return repo.update_user(user_id, update_data)

    def delete_user(self, user_id: int) -> None:
        with UserRepository() as repo:
            repo.delete_user(user_id)

    def get_all_users(self) -> list[Type[User]]:
        with UserRepository() as repo:
            return repo.get_all_users()
