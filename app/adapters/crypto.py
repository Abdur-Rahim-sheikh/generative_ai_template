from pwdlib import PasswordHash
from ..utils import singleton


@singleton
class PasswordHasher:
    def __init__(self):
        self.password_hasher = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self.password_hasher.hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        return self.password_hasher.verify(password, hashed)
