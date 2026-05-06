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
        self, text: str, output_format: BaseModel, instruction: str = ""
    ) -> BaseModel:
        app_logger.debug(f"{text=}, {instruction=}")
        response = output_format.model_json_schema()

        output = output_format.model_validate_json(response)
        return output
