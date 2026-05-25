from datetime import datetime, timedelta, timezone

import jwt

from ..utils import singleton


@singleton
class JwtManager:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def encode(
        self, data: dict, expires_delta: timedelta = timedelta(minutes=10)
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        return jwt.encode(
            {"exp": expire, **to_encode},
            self.secret_key,
            algorithm=self.algorithm,
        )

    def decode(self, token: str) -> dict:
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
