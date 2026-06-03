from typing import Annotated

from fastapi import Depends

from app.users.api.dependencies.get_current_user import get_current_user
from app.users.schemas.user_schema import UserInDB

# A provider is an authenticated application user. This alias makes the intent
# explicit at the provider-facing endpoints.
CurrentProvider = Annotated[UserInDB, Depends(get_current_user)]
