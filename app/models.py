from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime

DATABASE_URL = "sqlite:///aviation_ergonomics.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    login = Column(String, nullable=True)
    password = Column(String, nullable=True)
#
#
# class TestResult(Base):
#     __tablename__ = "test_results"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_name = Column(String, nullable=False)
#     test_type = Column(String, nullable=False)  # Например, PVT или NASA-TLX
#     result = Column(String, nullable=False)  # JSON-строка с результатами
#     timestamp = Column(DateTime, default=datetime.datetime.utcnow)
#
#
# class PVTResult(Base):
#     __tablename__ = "pvt_results"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     reaction_time = Column(Float, nullable=False)
#     user = relationship("User", back_populates="pvt_results")
#
#
# class NASA_TLX(Base):
#     __tablename__ = "nasa_tlx"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     mental_demand = Column(Integer, nullable=False)
#     physical_demand = Column(Integer, nullable=False)
#     temporal_demand = Column(Integer, nullable=False)
#     performance = Column(Integer, nullable=False)
#     effort = Column(Integer, nullable=False)
#     frustration = Column(Integer, nullable=False)
#     user = relationship("User", back_populates="nasa_tlx_results")

