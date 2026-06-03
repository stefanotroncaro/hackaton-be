from datetime import date
from uuid import UUID

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.models.base_class import Base
from app.patients.constants.patient_constants import (
    PATIENT_EMAIL_MAX_LENGTH,
    PATIENT_NAME_MAX_LENGTH,
)


class Patient(Base):
    __tablename__ = "patients"

    # The provider that invited this patient (an entry in the `users` table).
    provider_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    first_name: Mapped[str] = mapped_column(String(PATIENT_NAME_MAX_LENGTH))
    last_name: Mapped[str] = mapped_column(String(PATIENT_NAME_MAX_LENGTH))
    email: Mapped[str] = mapped_column(String(PATIENT_EMAIL_MAX_LENGTH))
    date_of_birth: Mapped[date]

    # One explicit column per intake question. There is intentionally no
    # generic answers blob: a new question requires a new column + migration.
    chief_complaint: Mapped[str]
    symptom_duration: Mapped[str]
    mood_rating: Mapped[int]
    symptoms: Mapped[list[str]] = mapped_column(JSON, default=list)
    current_medications: Mapped[str | None]
    past_psychiatric_history: Mapped[str | None]
    family_psychiatric_history: Mapped[str | None]
    substance_use: Mapped[str | None]
    suicidal_ideation: Mapped[bool]
