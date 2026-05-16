import asyncio

from pydantic import BaseModel

from ...interfaces import BaseLLM
from polyfactory.factories.pydantic_factory import ModelFactory


class DummyLLM(BaseLLM):
    """
    Synchronous, zero-latency LLM double for unit tests.

    Returns deterministic strings so tests can assert on content without
    calling a real model.  The singleton decorator has been intentionally
    omitted: each test should construct its own instance so state never
    leaks between test cases.
    """

    def __init__(self):
        # Record every call so tests can inspect what was sent to the LLM.
        self.call_history: list[dict] = []

    async def prepare(self):
        await asyncio.sleep(0)

    async def ask(self, text: str, instruction: str = "") -> str:
        self.call_history.append(
            {"text": text, "instruction": instruction, "method": self.ask.__name__}
        )
        return f"dummy response for: {text}"

    async def formatted_ask(
        self,
        text: str,
        output_format: type[BaseModel],
        instruction: str = "",
    ) -> BaseModel:
        self.call_history.append(
            {
                "text": text,
                "output_format": output_format,
                "instruction": instruction,
                "method": self.formatted_ask.__name__,
            }
        )

        class DynamicFactory(ModelFactory[output_format]):
            __model__ = output_format

        # constructing fake data
        return DynamicFactory.build()
