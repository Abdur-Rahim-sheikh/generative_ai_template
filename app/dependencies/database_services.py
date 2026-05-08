from fastapi import Depends

from ..config import get_async_session
from ..repositories import UnitOfWork
from ..services import UserService
from ..interfaces import BaseUnitOfWork


def get_unit_of_work(session=Depends(get_async_session)) -> BaseUnitOfWork:
    return UnitOfWork(session)


def get_user_service(
    uow: BaseUnitOfWork = Depends(get_unit_of_work),
):
    return UserService(uow)
