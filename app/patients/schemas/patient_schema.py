from datetime import date, datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.patients.constants.patient_constants import (
    PATIENT_EMAIL_MAX_LENGTH,
    PATIENT_NAME_MAX_LENGTH,
)
from app.patients.schemas.intake_schema import IntakeAnswers

_NameField = Field(min_length=1, max_length=PATIENT_NAME_MAX_LENGTH)
_EmailField = Field(max_length=PATIENT_EMAIL_MAX_LENGTH)


class PatientDemographics(BaseModel):
    first_name: Annotated[str, _NameField]
    last_name: Annotated[str, _NameField]
    email: Annotated[EmailStr, _EmailField]
    date_of_birth: date


class IntakeSubmissionRequest(PatientDemographics, IntakeAnswers):
    """Everything a patient submits when answering the intake form."""


class PatientCreate(PatientDemographics, IntakeAnswers):
    provider_id: UUID


class PatientUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class PatientInDB(PatientDemographics, IntakeAnswers):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    provider_id: UUID
    created_at: datetime


class PatientResponse(PatientInDB):
    pass


class PatientSummary(BaseModel):
    """Compact view used in the provider's patient list / dashboard."""

    model_config = ConfigDict(from_attributes=True)
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    date_of_birth: date
    chief_complaint: str
    created_at: datetime
