from uuid import UUID

from sqlalchemy.orm import Session

from app.patients.repositories.invitations_repository import (
    InvitationsRepository,
    invitations_repository,
)
from app.patients.schemas.invitation_schema import (
    InvitationCreate,
    InvitationInDB,
)


class InvitationsService:
    def __init__(
        self,
        session: Session,
        repository: InvitationsRepository = invitations_repository,
    ):
        self.session = session
        self.repository = repository

    def create_invitation(self, provider_id: UUID) -> InvitationInDB:
        created = self.repository.create(
            self.session, InvitationCreate(provider_id=provider_id)
        )
        return InvitationInDB.model_validate(created)

    def get_by_id(self, invitation_id: UUID) -> InvitationInDB | None:
        invitation = self.repository.get(self.session, invitation_id)
        if not invitation:
            return None
        return InvitationInDB.model_validate(invitation)
