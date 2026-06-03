from uuid import UUID

from sqlalchemy.orm import Session

from app.common.repositories.base_repository import BaseRepository
from app.common.schemas.pagination_schema import ListFilter, ListResponse
from app.patients.models.patient import Patient
from app.patients.schemas.patient_schema import PatientCreate, PatientUpdate


class PatientsRepository(
    BaseRepository[Patient, PatientCreate, PatientUpdate]
):
    def list_by_provider(
        self, db: Session, provider_id: UUID, list_options: ListFilter
    ) -> ListResponse:
        query = db.query(self.model).filter(
            Patient.provider_id == provider_id
        )
        return self.list(db, list_options, query=query)

    def count_by_provider(self, db: Session, provider_id: UUID) -> int:
        return (
            db.query(self.model)
            .filter(Patient.provider_id == provider_id)
            .count()
        )


patients_repository = PatientsRepository(Patient)
