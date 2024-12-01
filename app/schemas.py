# from pydantic import BaseModel, Field
#
# class UserSchema(BaseModel):
#     name: str = Field(..., max_length=100)
#     experiment_id: int
#
# class PVTResultSchema(BaseModel):
#     user_id: int
#     reaction_time: float
#
# class NASA_TLXSсhema(BaseModel):
#     user_id: int
#     mental_demand: int
#     physical_demand: int
#     temporal_demand: int
#     performance: int
#     effort: int
#     frustration: int


from pydantic import BaseModel
from typing import Dict


class PVTResultSchema(BaseModel):
    user_name: str
    reaction_time: float  # Время реакции в секундах


class NASATLXResultSchema(BaseModel):
    user_name: str
    scores: Dict[str, int]  # Оценки по каждому из параметров NASA-TLX
