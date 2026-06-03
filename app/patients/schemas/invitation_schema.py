from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.common.schemas.common_schemas import EmailBase


class InvitationRequest(EmailBase):
    pass


class InvitationCreate(BaseModel):
    provider_id: UUID


class InvitationUpdate(BaseModel):
    provider_id: UUID | None = None


class InvitationInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    provider_id: UUID


class InvitationResponse(BaseModel):
    invitation_token: UUID
    intake_url: str
