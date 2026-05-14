from abc import ABC, abstractmethod


class BaseVideo(ABC):
    @abstractmethod
    async def generate(
        self, prompt: str, duration: int, aspect_ratio: str, high_resolution: bool
    ) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    async def generate_with_reference_image(
        self,
        prompt: str,
        duration: int,
        aspect_ratio: str,
        high_resolution: bool,
        first_frame: bytes,
        last_frame: bytes | None = None,
    ) -> list[str]:
        raise NotImplementedError
