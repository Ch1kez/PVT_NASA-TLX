# app/schemas/UserSchema.py
from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Полное имя пользователя")
    login: str = Field(..., min_length=3, max_length=50, description="Логин пользователя")
    password: str = Field(..., min_length=4, description="Пароль пользователя")
