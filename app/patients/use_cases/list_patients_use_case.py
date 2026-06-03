from uuid import UUID

from sqlalchemy.orm import Session

from app.common.schemas.pagination_schema import ListFilter, ListResponse
from app.patients.services.patients_service import PatientsService


class ListPatientsUseCase:
    def __init__(self, session: Session):
        self.session = session

    def execute(
        self, provider_id: UUID, list_options: ListFilter
    ) -> ListResponse:
        return PatientsService(self.session).list_for_provider(
            provider_id, list_options
        )
