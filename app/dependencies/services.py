from fastapi import Depends

from ..config import get_async_session
from ..repositories import UserRepository
from ..services import UserService


def get_user_repository(session=Depends(get_async_session)):
    return UserRepository(session)


def get_user_service(user_repository=Depends(get_user_repository)):
    return UserService(user_repository)
