from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash


class Security:
    def __init__(self, secret_key: str, algorithm: str):
        self.password_hasher = PasswordHash.recommended()
        self.secret_key = secret_key
        self.algorithm = algorithm

    def hash_password(self, password: str) -> str:
        return self.password_hasher.hash(password)

    def verify_password(self, password: str, hashed: str) -> bool:
        return self.password_hasher.verify(password, hashed)

    def encode_access_token(
        self, data: dict, expires_delta: timedelta = timedelta(minutes=10)
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        return jwt.encode(
            {"exp": expire, **to_encode},
            self.secret_key,
            algorithm=self.algorithm,
        )

    def decode_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
