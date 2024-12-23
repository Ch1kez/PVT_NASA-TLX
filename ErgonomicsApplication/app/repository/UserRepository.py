# app/repository/UserRepository.py
from typing import Optional, Type
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.schemas.UserSchema import UserSchema
from app.database.models import User
from app.database.database import SessionLocal


class UserRepository:
    def __init__(self):
        self.db: Session = None

    def __enter__(self):
        self.db = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.db:
            self.db.close()

    def is_login_exists(self, login: str) -> bool:
        return self.db.query(User).filter(User.login == login).first() is not None

    def create_user(self, user_data: dict) -> int:
        try:
            validated_data = UserSchema(**user_data)
        except ValidationError as e:
            error_details = [
                {"field": err["loc"][0], "message": err["msg"]}
                for err in e.errors()
            ]
            raise ValueError(f"Ошибка валидации: {error_details}")

        if self.is_login_exists(validated_data.login):
            raise ValueError("Пользователь с таким логином уже существует!")

        user = User(**validated_data.dict())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user.id

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def check_user(self, login: str, password: str) -> str | None:
        return self.db.query(User.name).filter(User.login == login, User.password == password).scalar()

    def check_user_with_id(self, login: str, password: str) -> tuple[str, int] | None:
        """
        Возвращает (name, id) если пользователь найден,
        иначе None.
        """
        user = (
            self.db.query(User)
            .filter(User.login == login, User.password == password)
            .first()
        )
        if user:
            return (user.name, user.id)
        return None

    def update_user(self, user_id: int, update_data: dict) -> User:
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
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("Пользователь с таким ID не найден.")
        self.db.delete(user)
        self.db.commit()

    def get_all_users(self) -> list[Type[User]]:
        return self.db.query(User).all()
