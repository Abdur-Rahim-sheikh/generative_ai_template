from fastapi import Depends

from ..config import get_async_session
from ..repositories import UnitOfWork
from ..services import UserService, ProductService
from ..interfaces import BaseUnitOfWork
from ..adapters.security import Security
from ..config import settings


def get_unit_of_work(session=Depends(get_async_session)) -> BaseUnitOfWork:
    return UnitOfWork(session)


def get_security():
    return Security(settings.JWT_SECRET_KEY.get_secret_value(), settings.JWT_ALGORITHM)


def get_user_service(
    uow: BaseUnitOfWork = Depends(get_unit_of_work),
    security: Security = Depends(get_security),
):
    return UserService(uow, security)


def get_product_service(
    uow: BaseUnitOfWork = Depends(get_unit_of_work),
):
    return ProductService(uow)
