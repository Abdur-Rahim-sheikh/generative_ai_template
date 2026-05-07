from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from sqlmodel import Session as SQLModelSession

from ..domain import Session, Transaction, User, Wallet, Product

T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    def __init__(self, session: SQLModelSession):
        self.session = session

    @abstractmethod
    async def save(self, data: T) -> T:
        pass

    @abstractmethod
    async def get(self, id: UUID) -> T:
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        pass


class BaseUserRepository(BaseRepository[User]):
    @abstractmethod
    async def get_by_email(self, email: str) -> User:
        pass


class BaseProductRepository(BaseRepository[Product]):
    pass


class BaseWalletRepository(BaseRepository[Wallet]):
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Wallet:
        pass


class BaseTransactionRepository(BaseRepository[Transaction]):
    @abstractmethod
    async def get_by_wallet_id(self, wallet_id: UUID) -> list[Transaction]:
        pass


class BaseSessionRepository(BaseRepository[Session]):
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Session:
        pass
