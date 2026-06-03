from pydantic import BaseModel

from app.patients.schemas.patient_schema import PatientSummary


class ProviderDashboardResponse(BaseModel):
    total_patients: int
    recent_patients: list[PatientSummary]
