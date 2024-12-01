from typing import Optional, Type
from pydantic import ValidationError
from sqlalchemy.orm import Session
from .schemas import UserSchema
from app.models import User, SessionLocal


class DatabaseSession:
    def __init__(self):
        self.db: Optional[Session] = None

    def __enter__(self):
        self.db = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.db:
            self.db.close()


class UserRepository(DatabaseSession):
    def create_user(self, user_data: dict) -> User:
        """
        Создает пользователя в базе данных.
        :param user_data: Данные пользователя в виде словаря.
        :return: Объект User.
        """
        if not self.db:
            raise ValueError("Сессия базы данных не инициализирована.")

        try:
            # Валидация входных данных
            validated_data = UserSchema(**user_data)
        except ValidationError as e:
            # Структурированная ошибка с деталями
            error_details = [
                {"field": err["loc"][0], "message": err["msg"]}
                for err in e.errors()
            ]
            raise ValueError(f"Ошибка валидации: {error_details}")

        # Сохранение пользователя
        user = User(**validated_data.dict())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Получает пользователя по ID.
        :param user_id: ID пользователя.
        :return: Объект User или None.
        """
        if not self.db:
            raise ValueError("Сессия базы данных не инициализирована.")

        return self.db.query(User).filter(User.id == user_id).first()

    def update_user(self, user_id: int, update_data: dict) -> User:
        """
        Обновляет данные пользователя.
        :param user_id: ID пользователя.
        :param update_data: Данные для обновления.
        :return: Объект User.
        """
        if not self.db:
            raise ValueError("Сессия базы данных не инициализирована.")

        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("Пользователь с таким ID не найден.")

        try:
            validated_data = UserSchema(**update_data)
        except ValidationError as e:
            raise ValueError(f"Ошибка валидации: {e}")

        for key, value in validated_data.dict(exclude_unset=True).items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> None:
        """
        Удаляет пользователя из базы данных.
        :param user_id: ID пользователя.
        """
        if not self.db:
            raise ValueError("Сессия базы данных не инициализирована.")

        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("Пользователь с таким ID не найден.")

        self.db.delete(user)
        self.db.commit()

    def get_all_users(self) -> list[Type[User]]:
        """
        Возвращает список всех пользователей.
        :return: Список объектов User.
        """
        if not self.db:
            raise ValueError("Сессия базы данных не инициализирована.")

        return self.db.query(User).all()
