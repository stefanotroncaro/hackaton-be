from uuid import UUID

from sqlalchemy.orm import Session

from app.common.schemas.pagination_schema import ListFilter, ListResponse
from app.patients.repositories.patients_repository import (
    PatientsRepository,
    patients_repository,
)
from app.patients.schemas.patient_schema import PatientCreate, PatientInDB


class PatientsService:
    def __init__(
        self,
        session: Session,
        repository: PatientsRepository = patients_repository,
    ):
        self.session = session
        self.repository = repository

    def create_patient(self, patient: PatientCreate) -> PatientInDB:
        created_patient = self.repository.create(self.session, patient)
        return PatientInDB.model_validate(created_patient)

    def list_for_provider(
        self, provider_id: UUID, list_options: ListFilter
    ) -> ListResponse:
        return self.repository.list_by_provider(
            self.session, provider_id, list_options
        )

    def count_for_provider(self, provider_id: UUID) -> int:
        return self.repository.count_by_provider(self.session, provider_id)
