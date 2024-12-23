# app/services/TestService.py
from typing import List
from app.repository.TestRepository import TestRepository
from app.database.models import PVTResult, NASATLXResult


class TestService:

    def save_pvt_round(
        self,
        user_id: int,
        exercise_name: str,
        task_number: str,
        type_test: str,
        round_index: int,
        reaction_time: float
    ) -> PVTResult:
        with TestRepository() as repo:
            return repo.save_pvt_round(
                user_id=user_id,
                exercise_name=exercise_name,
                task_number=task_number,
                type_test=type_test,
                round_index=round_index,
                reaction_time=reaction_time
            )

    def get_pvt_results_for_user(self, user_id: int) -> List[PVTResult]:
        with TestRepository() as repo:
            return repo.get_pvt_results_for_user(user_id)

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
        with TestRepository() as repo:
            return repo.save_nasa_tlx_result(
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

    def get_nasa_tlx_results_for_user(self, user_id: int) -> List[NASATLXResult]:
        with TestRepository() as repo:
            return repo.get_nasa_tlx_results_for_user(user_id)
