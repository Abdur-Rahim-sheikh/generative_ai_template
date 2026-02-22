from abc import ABC, abstractmethod


class NoSQL(ABC):
    @abstractmethod
    async def connect(self):
        raise NotImplementedError("implement the connect method")

    @abstractmethod
    async def disconnect(self):
        raise NotImplementedError("implement the disconnect method")

    @abstractmethod
    async def set_data(
        self, key: str, value: str | bytes | bytearray, exp: int = 604800
    ):
        raise NotImplementedError("Implement the set method")

    @abstractmethod
    async def get_data(self, key: str):
        raise NotImplementedError("implement the get method")
