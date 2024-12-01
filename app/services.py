# from sqlalchemy.orm import Session
# from .models import User, PVTResult, NASA_TLX
# from .schemas import UserSchema, PVTResultSchema, NASA_TLXSсhema
#
# def create_user(db: Session, user: UserSchema):
#     db_user = User(name=user.name, experiment_id=user.experiment_id)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
# def save_pvt_result(db: Session, result: PVTResultSchema):
#     db_result = PVTResult(user_id=result.user_id, reaction_time=result.reaction_time)
#     db.add(db_result)
#     db.commit()
#     db.refresh(db_result)
#     return db_result
#
#


from sqlalchemy.orm import Session
from app.models import TestResult
from app.schemas import PVTResultSchema, NASATLXResultSchema
import json

def save_pvt_result(db: Session, result: PVTResultSchema):
    db_result = TestResult(
        user_name=result.user_name,
        test_type="PVT",
        result=json.dumps({"reaction_time": result.reaction_time}),
    )
    db.add(db_result)
    db.commit()

def save_nasa_tlx_result(db: Session, result: NASATLXResultSchema):
    db_result = TestResult(
        user_name=result.user_name,
        test_type="NASA-TLX",
        result=json.dumps(result.scores),
    )
    db.add(db_result)
    db.commit()

def get_test_results(db: Session):
    return db.query(TestResult).all()
