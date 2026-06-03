from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.common.models.base_class import Base


class Invitation(Base):
    __tablename__ = "invitations"

    provider_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
