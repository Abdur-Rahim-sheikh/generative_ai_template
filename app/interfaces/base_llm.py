from abc import ABC, abstractmethod

from pydantic import BaseModel


class BaseLLM(ABC):
    @abstractmethod
    async def ask(self, text: str, instruction: str = "") -> str:
        raise NotImplementedError

    @abstractmethod
    async def formatted_ask(
        self, text: str, output_format: BaseModel, instruction: str = ""
    ) -> BaseModel:
        raise NotImplementedError
