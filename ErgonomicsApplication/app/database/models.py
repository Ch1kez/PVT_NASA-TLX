import datetime

from .database import Base

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    login = Column(String, nullable=True)
    password = Column(String, nullable=True)


class PVTResult(Base):
    __tablename__ = "pvt_results"
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="pvt_results")

    exercise_name = Column(String, nullable=False)  # Взлет/Посадка и т.д.
    task_number = Column(String, nullable=False)    # Номер задачи (1,2,3)

    type_test = Column(String, nullable=True)       # "before"/"after"
    round_index = Column(Integer, nullable=True)    # Номер раунда (0..N)
    reaction_time = Column(Float, nullable=True)    # Время реакции (сек)

    timestamp = Column(DateTime, default=datetime.datetime.utcnow)  # Когда проходили


class NASATLXResult(Base):
    __tablename__ = "nasa_tlx_results"
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="nasa_tlx_results")

    exercise_name = Column(String, nullable=False)
    task_number = Column(String, nullable=False)

    # Сырые оценки (0..100) — можно хранить как int
    mental_demand = Column(Integer, nullable=True)
    physical_demand = Column(Integer, nullable=True)
    temporal_demand = Column(Integer, nullable=True)
    performance = Column(Integer, nullable=True)
    effort = Column(Integer, nullable=True)
    frustration = Column(Integer, nullable=True)

    # Вес каждой шкалы (0..5)
    weight_mental = Column(Integer, nullable=True)
    weight_physical = Column(Integer, nullable=True)
    weight_temporal = Column(Integer, nullable=True)
    weight_performance = Column(Integer, nullable=True)
    weight_effort = Column(Integer, nullable=True)
    weight_frustration = Column(Integer, nullable=True)

    # Итоговый Weighted TLX
    weighted_tlx = Column(Float, nullable=True)

    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
