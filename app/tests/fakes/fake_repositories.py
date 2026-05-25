from typing import Generic, TypeVar
from uuid import UUID, uuid4

from ...domain.models import Product, Transaction, User, UserSession, Wallet
from ...interfaces.base_repository import (
    BaseProductRepository,
    BaseTransactionRepository,
    BaseUserRepository,
    BaseUserSessionRepository,
    BaseWalletRepository,
)
from ...interfaces.base_uow import BaseUnitOfWork

T = TypeVar("T")


class GenericFakeRepository(Generic[T]):
    def __init__(self):
        self._storage: dict[UUID, T] = {}

    async def save(self, data: T):
        if not data.id:
            data.id = uuid4()

        self._storage[data.id] = data

    async def get(self, id: UUID) -> T | None:
        return self._storage.get(id)

    async def delete(self, id: UUID) -> None:
        self._storage.pop(id, None)


class FakeUserRepository(GenericFakeRepository[User], BaseUserRepository):
    """In-memory User repository for unit tests."""

    async def get_by_email(self, email: str) -> User | None:
        for user in self._storage.values():
            if user.email == email:
                return user
        return None


class FakeProductRepository(GenericFakeRepository[Product], BaseProductRepository):
    """In-memory Product repository for unit tests."""

    async def get_by_title(self, title: str) -> Product | None:
        for product in self._storage.values():
            if product.title == title:
                return product
        return None


class FakeWalletRepository(GenericFakeRepository[Wallet], BaseWalletRepository):
    """In-memory Wallet repository for unit tests."""

    async def get_by_user_id(self, user_id: UUID) -> Wallet | None:
        for wallet in self._storage.values():
            if wallet.user_id == user_id:
                return wallet
        return None


class FakeTransactionRepository(
    GenericFakeRepository[Transaction], BaseTransactionRepository
):
    """In-memory Transaction repository for unit tests."""

    async def get_by_wallet_id(self, wallet_id: UUID) -> list[Transaction]:
        return [t for t in self._storage.values() if t.wallet_id == wallet_id]


class FakeUserSessionRepository(
    GenericFakeRepository[UserSession], BaseUserSessionRepository
):
    """In-memory Session repository for unit tests."""

    async def get_by_user_id(self, user_id: UUID) -> UserSession | None:
        for session in self._storage.values():
            if session.user_id == user_id:
                return session
        return None


class FakeUnitOfWork(BaseUnitOfWork):
    """
    In-memory UoW that wires together all fake repositories.
    Tracks commit/rollback calls so tests can assert on them.
    """

    def __init__(self):
        self.users = FakeUserRepository()
        self.products = FakeProductRepository()
        self.wallets = FakeWalletRepository()
        self.transactions = FakeTransactionRepository()
        self.sessions = FakeUserSessionRepository()

        self.committed = False
        self.rolled_back = False
        self.flushed = False

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True

    async def __aenter__(self):
        self.committed = False
        self.rolled_back = False
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def flush(self):
        self.flushed = True
