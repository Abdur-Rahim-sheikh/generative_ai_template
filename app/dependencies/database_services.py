from fastapi import Depends

from ..config import get_async_session
from ..repositories import UserRepository
from ..services import UserService
from ..interfaces.base_repository import BaseUserRepository


def get_user_repository(session=Depends(get_async_session)) -> BaseUserRepository:
    return UserRepository(session)


def get_user_service(
    user_repository: BaseUserRepository = Depends(get_user_repository),
):
    return UserService(user_repository)
