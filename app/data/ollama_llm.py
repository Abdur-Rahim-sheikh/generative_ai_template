from ollama import AsyncClient, GenerateResponse, ResponseError
from pydantic import BaseModel

from ..interfaces import BaseLLM
from ..utils import singleton
from ..config import app_logger


@singleton
class OllamaLLM(BaseLLM):
    def __init__(self, host: str, model: str = "llama3.1:8b", keep_alive: str = "5m"):
        self.client = AsyncClient(host=host)
        self.model = model
        self.keep_alive = keep_alive

    async def prepare(self):
        try:
            await self.client.pull(self.model)
        except ResponseError as e:
            app_logger.exception(msg="ollama could not pull the base model")
            raise RuntimeError("Ollama could not be prepared") from e

    async def ask(self, text: str, instruction: str = "") -> str:
        try:
            response: GenerateResponse = await self.client.generate(
                model=self.model,
                prompt=text,
                system=instruction,
                keep_alive=self.keep_alive,
            )

        except ResponseError as e:
            raise RuntimeError("Request could not be fullfilled") from e

        return response.response

    async def formatted_ask(
        self, text: str, output_format: BaseModel, instruction: str = ""
    ) -> BaseModel:
        try:
            response: GenerateResponse = await self.client.generate(
                model=self.model,
                prompt=text,
                system=instruction,
                format=output_format.model_json_schema(),
                keep_alive=self.keep_alive,
            )

        except ResponseError as e:
            raise RuntimeError("Request could not be fullfilled") from e

        output = output_format.model_validate_json(response.response)
        return output
