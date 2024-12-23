# app/repository/TestRepository.py

from typing import List
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.database.models import PVTResult, NASATLXResult


class TestRepository:
    def __init__(self):
        self.db: Session = None

    def __enter__(self):
        self.db = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.close()

    # ---------- PVT ----------

    def save_pvt_round(
        self,
        user_id: int,
        exercise_name: str,
        task_number: str,
        type_test: str,
        round_index: int,
        reaction_time: float
    ) -> PVTResult:
        """
        Сохраняет один раунд PVT-теста.
        Возвращает объект PVTResult.
        """
        result = PVTResult(
            user_id=user_id,
            exercise_name=exercise_name,
            task_number=task_number,
            type_test=type_test,
            round_index=round_index,
            reaction_time=reaction_time
        )
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result

    def get_pvt_results_for_user(self, user_id: int) -> List[PVTResult]:
        return (
            self.db.query(PVTResult)
            .filter(PVTResult.user_id == user_id)
            .order_by(PVTResult.timestamp.desc())
            .all()
        )

    # ---------- NASA-TLX ----------

    def save_nasa_tlx_result(
        self,
        user_id: int,
        exercise_name: str,
        task_number: str,
        mental_demand: int,
        physical_demand: int,
        temporal_demand: int,
        performance: int,
        effort: int,
        frustration: int,
        weight_mental: int,
        weight_physical: int,
        weight_temporal: int,
        weight_performance: int,
        weight_effort: int,
        weight_frustration: int,
        weighted_tlx: float
    ) -> NASATLXResult:
        """
        Сохраняет итог NASA-TLX вместе с сырыми баллами и весами.
        """
        result = NASATLXResult(
            user_id=user_id,
            exercise_name=exercise_name,
            task_number=task_number,
            mental_demand=mental_demand,
            physical_demand=physical_demand,
            temporal_demand=temporal_demand,
            performance=performance,
            effort=effort,
            frustration=frustration,
            weight_mental=weight_mental,
            weight_physical=weight_physical,
            weight_temporal=weight_temporal,
            weight_performance=weight_performance,
            weight_effort=weight_effort,
            weight_frustration=weight_frustration,
            weighted_tlx=weighted_tlx
        )
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result

    def get_nasa_tlx_results_for_user(self, user_id: int) -> List[NASATLXResult]:
        return (
            self.db.query(NASATLXResult)
            .filter(NASATLXResult.user_id == user_id)
            .order_by(NASATLXResult.timestamp.desc())
            .all()
        )