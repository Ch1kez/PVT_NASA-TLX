# app/schemas/TestResultsSchema.py
from typing import Dict
from pydantic import BaseModel

class PVTResultSchema(BaseModel):
    user_name: str
    reaction_time: float  # Время реакции в секундах

class NASATLXResultSchema(BaseModel):
    user_name: str
    scores: Dict[str, int]  # Оценки по каждому из параметров NASA-TLX
