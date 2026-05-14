from abc import ABC, abstractmethod


class BaseImageGenerator(ABC):
    @abstractmethod
    async def generate(
        self, prompt: str, width: int, height: int, batch: int = 1
    ) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    async def edit(
        self,
        prompt: str,
        reference_image: bytes,
        width: int,
        height: int,
        batch: int = 1,
    ) -> list[str]:
        raise NotImplementedError
