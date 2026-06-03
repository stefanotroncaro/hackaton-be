from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.common.api.dependencies.get_session import SessionDependency
from app.common.schemas.pagination_schema import ListFilter, ListResponse
from app.patients.api.dependencies.get_current_provider import CurrentProvider
from app.patients.constants.intake_form import PSYCHIATRIC_INTAKE_FORM
from app.patients.schemas.dashboard_schema import ProviderDashboardResponse
from app.patients.schemas.intake_schema import (
    PsychiatricIntakeFormDefinition,
)
from app.patients.schemas.invitation_schema import (
    InvitationRequest,
    InvitationResponse,
)
from app.patients.schemas.patient_schema import (
    IntakeSubmissionRequest,
    PatientResponse,
    PatientSummary,
)
from app.patients.use_cases.create_invitation_use_case import (
    CreateInvitationUseCase,
)
from app.patients.use_cases.get_dashboard_use_case import GetDashboardUseCase
from app.patients.use_cases.list_patients_use_case import ListPatientsUseCase
from app.patients.use_cases.submit_intake_use_case import SubmitIntakeUseCase

router = APIRouter()


@router.get("/intake-form", status_code=status.HTTP_200_OK)
def get_intake_form() -> PsychiatricIntakeFormDefinition:
    """Public: the psychiatric intake form definition for client rendering."""
    return PSYCHIATRIC_INTAKE_FORM


@router.post("/invitations", status_code=status.HTTP_201_CREATED)
def create_invitation(
    session: SessionDependency,
    provider: CurrentProvider,
    invitation_request: InvitationRequest,
) -> InvitationResponse:
    """Provider: invite a prospective patient and email them the intake link."""
    return CreateInvitationUseCase(session).execute(
        provider.id, invitation_request.email
    )


@router.post("/intake", status_code=status.HTTP_201_CREATED)
def submit_intake(
    session: SessionDependency,
    submission: IntakeSubmissionRequest,
    invitation_token: Annotated[UUID, Query()],
) -> PatientResponse:
    """Public: a patient answers the intake form using an invitation token and
    is registered under the provider that invited them."""
    return SubmitIntakeUseCase(session).execute(invitation_token, submission)


@router.get("", status_code=status.HTTP_200_OK)
def list_patients(
    session: SessionDependency,
    provider: CurrentProvider,
    list_options: Annotated[ListFilter, Query()],
) -> ListResponse[PatientSummary]:
    """Provider: list the patients that answered this provider's intake."""
    return ListPatientsUseCase(session).execute(provider.id, list_options)


@router.get("/dashboard", status_code=status.HTTP_200_OK)
def get_dashboard(
    session: SessionDependency,
    provider: CurrentProvider,
) -> ProviderDashboardResponse:
    """Provider: summary view of their patients for the dashboard."""
    return GetDashboardUseCase(session).execute(provider.id)
