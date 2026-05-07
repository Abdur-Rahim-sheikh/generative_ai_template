import bcrypt
from pydantic import BaseModel, EmailStr, SecretStr


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class CreateUserRequest(BaseUser):
    password: SecretStr

    @property
    def hashed_password(self) -> str:
        pwd_bytes = self.password.get_secret_value().encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pwd_bytes, salt)
        return hashed.decode("utf-8")
