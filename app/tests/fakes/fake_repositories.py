from uuid import uuid4, UUID

from ...domain import User, Product, Wallet, Transaction, UserSession
from ...interfaces.base_repository import (
    BaseUserRepository,
    BaseProductRepository,
    BaseWalletRepository,
    BaseTransactionRepository,
    BaseUserSessionRepository,
)
from ...interfaces.base_uow import BaseUnitOfWork


class FakeUserRepository(BaseUserRepository):
    """In-memory User repository for unit tests."""

    def __init__(self):
        self.users: dict[UUID, User] = {}

    async def save(self, data: User) -> User:

        data.id = uuid4()
        self.users[data.id] = data
        return data

    async def get(self, id: UUID) -> User | None:
        return self.users.get(id)

    async def delete(self, id: UUID) -> None:
        self.users.pop(id, None)

    async def get_by_email(self, email: str) -> User | None:
        for user in self.users.values():
            if user.email == email:
                return user
        return None


class FakeProductRepository(BaseProductRepository):
    """In-memory Product repository for unit tests."""

    def __init__(self):
        self.products: dict[UUID, Product] = {}

    async def save(self, data: Product) -> Product:
        data.id = uuid4()
        self.products[data.id] = data
        return data

    async def get(self, id: UUID) -> Product | None:
        return self.products.get(id)

    async def delete(self, id: UUID) -> None:
        self.products.pop(id, None)


class FakeWalletRepository(BaseWalletRepository):
    """In-memory Wallet repository for unit tests."""

    def __init__(self):
        self.wallets: dict[UUID, Wallet] = {}

    async def save(self, data: Wallet) -> Wallet:
        data.id = uuid4()
        self.wallets[data.id] = data
        return data

    async def get(self, id: UUID) -> Wallet | None:
        return self.wallets.get(id)

    async def delete(self, id: UUID) -> None:
        self.wallets.pop(id, None)

    async def get_by_user_id(self, user_id: UUID) -> Wallet | None:
        for wallet in self.wallets.values():
            if wallet.user_id == user_id:
                return wallet
        return None


class FakeTransactionRepository(BaseTransactionRepository):
    """In-memory Transaction repository for unit tests."""

    def __init__(self):
        self.transactions: dict[UUID, Transaction] = {}

    async def save(self, data: Transaction) -> Transaction:
        data.id = uuid4()
        self.transactions[data.id] = data
        return data

    async def get(self, id: UUID) -> Transaction | None:
        return self.transactions.get(id)

    async def delete(self, id: UUID) -> None:
        self.transactions.pop(id, None)

    async def get_by_wallet_id(self, wallet_id: UUID) -> list[Transaction]:
        return [t for t in self.transactions.values() if t.wallet_id == wallet_id]


class FakeSessionRepository(BaseUserSessionRepository):
    """In-memory Session repository for unit tests."""

    def __init__(self):
        self.sessions: dict[UUID, UserSession] = {}

    async def save(self, data: UserSession) -> UserSession:
        self.sessions[data.session_token] = data
        return data

    async def get(self, id: UUID) -> UserSession | None:
        return self.sessions.get(id)

    async def delete(self, id: UUID) -> None:
        self.sessions.pop(id, None)

    async def get_by_user_id(self, user_id: UUID) -> UserSession | None:
        for session in self.sessions.values():
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
        self.sessions = FakeSessionRepository()

        self.committed = False
        self.rolled_back = False

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
