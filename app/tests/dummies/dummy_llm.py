from pydantic import BaseModel

from ...interfaces import BaseLLM
from ...utils import singleton
from ...config import app_logger
import asyncio


@singleton
class DummyLLM(BaseLLM):
    async def prepare(self):
        await asyncio.sleep(2)

    async def ask(self, text: str, instruction: str = "") -> str:
        response = f"{instruction=} --\n dummy \n {text=}"

        return response

    async def formatted_ask(
        self, text: str, output_format: type[BaseModel], instruction: str = ""
    ) -> BaseModel:
        app_logger.debug(f"{text=}, {instruction=}")
        data = output_format.model_construct()
        # changes
        return data
