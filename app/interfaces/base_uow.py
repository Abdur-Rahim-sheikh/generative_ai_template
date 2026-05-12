from abc import ABC, abstractmethod
from typing import Self
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
    async def flush(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError
