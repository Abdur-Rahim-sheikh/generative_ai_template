from abc import ABC, abstractmethod

from ..schemas.script import SpeechSegment


class BaseTTS(ABC):
    @abstractmethod
    def has_language(self, language_code: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def allowed_languages(self) -> list[tuple[str, str]]:
        raise NotImplementedError

    @abstractmethod
    async def synthesize(self, segments: SpeechSegment) -> bytes:
        raise NotImplementedError
