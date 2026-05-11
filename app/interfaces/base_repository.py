from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ..domain import Product, UserSession, Transaction, User, Wallet

T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def save(self, data: T):
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: UUID) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        raise NotImplementedError


class BaseUserRepository(BaseRepository[User]):
    @abstractmethod
    async def get_by_email(self, email: str) -> User:
        raise NotImplementedError


class BaseProductRepository(BaseRepository[Product]):
    pass


class BaseWalletRepository(BaseRepository[Wallet]):
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Wallet:
        raise NotADirectoryError


class BaseTransactionRepository(BaseRepository[Transaction]):
    @abstractmethod
    async def get_by_wallet_id(self, wallet_id: UUID) -> list[Transaction]:
        raise NotImplementedError


class BaseUserSessionRepository(BaseRepository[UserSession]):
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> UserSession:
        raise NotImplementedError
