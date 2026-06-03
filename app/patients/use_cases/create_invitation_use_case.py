from uuid import UUID

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.emails.services.emails_service import EmailService
from app.patients.schemas.invitation_schema import InvitationResponse
from app.patients.services.invitations_service import InvitationsService

settings = get_settings()


class CreateInvitationUseCase:
    def __init__(self, session: Session):
        self.session = session

    def execute(
        self, provider_id: UUID, recipient_email: str
    ) -> InvitationResponse:
        invitation = InvitationsService(self.session).create_invitation(
            provider_id
        )
        server_host = str(settings.SERVER_HOST).rstrip("/")
        intake_url = (
            f"{server_host}{settings.API_V1_STR}"
            f"/patients/intake?invitation_token={invitation.id}"
        )

        EmailService().send_intake_invitation_email(
            recipient_email, intake_url
        )

        return InvitationResponse(
            invitation_token=invitation.id,
            intake_url=intake_url,
        )
