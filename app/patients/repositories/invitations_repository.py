from app.common.repositories.base_repository import BaseRepository
from app.patients.models.invitation import Invitation
from app.patients.schemas.invitation_schema import (
    InvitationCreate,
    InvitationUpdate,
)


class InvitationsRepository(
    BaseRepository[Invitation, InvitationCreate, InvitationUpdate]
):
    pass


invitations_repository = InvitationsRepository(Invitation)
