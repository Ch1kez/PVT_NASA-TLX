from typing import Optional, Type
from app.repository import UserRepository
from app.models import User


class UserService:
    def create_user(self, user_data: dict) -> User:
        """
        Создает пользователя, валидирует данные и сохраняет в базе данных.
        :param user_data: Данные пользователя.
        :return: Созданный пользователь.
        """
        with UserRepository() as repo:
            try:
                return repo.create_user(user_data)
            except ValueError as e:
                # Прокидываем ошибки дальше для обработки в интерфейсе
                raise e
            except Exception as e:
                # Общая обработка ошибок
                raise ValueError("Неизвестная ошибка при создании пользователя") from e

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Получает пользователя по ID.
        :param user_id: ID пользователя.
        :return: Пользователь или None.
        """
        with UserRepository() as repo:
            return repo.get_user_by_id(user_id)

    def update_user(self, user_id: int, update_data: dict) -> User:
        """
        Обновляет данные пользователя.
        :param user_id: ID пользователя.
        :param update_data: Данные для обновления.
        :return: Обновленный пользователь.
        """
        with UserRepository() as repo:
            return repo.update_user(user_id, update_data)

    def delete_user(self, user_id: int) -> None:
        """
        Удаляет пользователя по ID.
        :param user_id: ID пользователя.
        """
        with UserRepository() as repo:
            repo.delete_user(user_id)

    def get_all_users(self) -> list[Type[User]]:
        """
        Возвращает список всех пользователей.
        :return: Список пользователей.
        """
        with UserRepository() as repo:
            return repo.get_all_users()


class Services:
    user = UserService()

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
