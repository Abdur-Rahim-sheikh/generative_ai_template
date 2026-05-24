from typing import Annotated

from fastapi import Depends, HTTPException, status

from ..adapters import Security
from ..config.settings_config import OAUTH2_SCHEME
from .database_services import get_security

exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def decode_access_token(
    token: Annotated[str, Depends(OAUTH2_SCHEME)],
    security: Annotated[Security, Depends(get_security)],
) -> dict:

    try:
        payload = security.decode_access_token(token)
        return payload
    except Exception:
        raise exception


def get_user_wallet_id(
    payload: Annotated[dict, Depends(decode_access_token)],
) -> str:
    wallet_id = payload.get("wallet_id")
    if wallet_id is None:
        raise exception
    return wallet_id


def get_user_id(
    payload: Annotated[dict, Depends(decode_access_token)],
) -> str:
    user_id = payload.get("sub")
    if user_id is None:
        raise exception
    return user_id
