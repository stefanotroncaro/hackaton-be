from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.patients.schemas.patient_schema import (
    IntakeSubmissionRequest,
    PatientCreate,
    PatientResponse,
)
from app.patients.services.invitations_service import InvitationsService
from app.patients.services.patients_service import PatientsService


class SubmitIntakeUseCase:
    def __init__(self, session: Session):
        self.session = session

    def execute(
        self, invitation_token: UUID, submission: IntakeSubmissionRequest
    ) -> PatientResponse:
        invitation = InvitationsService(self.session).get_by_id(
            invitation_token
        )
        if not invitation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitation not found.",
            )

        created_patient = PatientsService(self.session).create_patient(
            PatientCreate(
                provider_id=invitation.provider_id,
                **submission.model_dump(),
            )
        )
        return PatientResponse.model_validate(
            created_patient, from_attributes=True
        )
