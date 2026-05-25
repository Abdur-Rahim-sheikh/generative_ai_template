from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, SecretStr


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class CreateUserRequest(BaseUser):
    password: SecretStr


class ReadUser(BaseUser):
    id: UUID
    is_active: bool
    created_at: datetime
