from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    def save(self, data):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def delete(self, id):
        pass


class BaseUserRepository(BaseRepository):
    @abstractmethod
    def get_by_email(self, email: str):
        pass


class BaseProductRepository(BaseRepository):
    pass


class BaseWalletRepository(BaseRepository):
    @abstractmethod
    def get_by_user_id(self, user_id):
        pass


class BaseTransactionRepository(BaseRepository):
    @abstractmethod
    def get_by_wallet_id(self, wallet_id):
        pass


class BaseSessionRepository(BaseRepository):
    @abstractmethod
    def get_by_user_id(self, user_id):
        pass
