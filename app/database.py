from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, engine


def init_db():
    Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
