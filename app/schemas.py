from typing import Dict
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Полное имя пользователя")
    login: str = Field(..., min_length=3, max_length=50, description="Логин пользователя")
    password: str = Field(..., min_length=4, description="Пароль пользователя")


class PVTResultSchema(BaseModel):
    user_id: int
    reaction_time: float


class NASA_TLXSсhema(BaseModel):
    user_id: int
    mental_demand: int
    physical_demand: int
    temporal_demand: int
    performance: int
    effort: int
    frustration: int


class PVTResultSchema(BaseModel):
    user_name: str
    reaction_time: float  # Время реакции в секундах


class NASATLXResultSchema(BaseModel):
    user_name: str
    scores: Dict[str, int]  # Оценки по каждому из параметров NASA-TLX
