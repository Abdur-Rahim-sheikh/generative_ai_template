from abc import ABC, abstractmethod

from .base_repository import (
    BaseProductRepository,
    BaseUserRepository,
    BaseTransactionRepository,
    BaseUserSessionRepository,
    BaseWalletRepository,
)


class BaseUnitOfWork(ABC):
    users: BaseUserRepository
    products: BaseProductRepository
    transactions: BaseTransactionRepository
    user_sessions: BaseUserSessionRepository
    wallets: BaseWalletRepository

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError
