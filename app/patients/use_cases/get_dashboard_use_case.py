from uuid import UUID

from sqlalchemy.orm import Session

from app.common.schemas.pagination_schema import ListFilter
from app.patients.schemas.dashboard_schema import ProviderDashboardResponse
from app.patients.schemas.patient_schema import PatientSummary
from app.patients.services.patients_service import PatientsService

RECENT_PATIENTS_LIMIT = 5


class GetDashboardUseCase:
    def __init__(self, session: Session):
        self.session = session

    def execute(self, provider_id: UUID) -> ProviderDashboardResponse:
        service = PatientsService(self.session)
        total = service.count_for_provider(provider_id)
        recent = service.list_for_provider(
            provider_id,
            ListFilter(
                page=1,
                page_size=RECENT_PATIENTS_LIMIT,
                order="desc",
                order_by="created_at",
            ),
        )
        return ProviderDashboardResponse(
            total_patients=total,
            recent_patients=[
                PatientSummary.model_validate(patient)
                for patient in recent.data
            ],
        )
