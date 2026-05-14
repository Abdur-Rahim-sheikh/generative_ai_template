import asyncio

from pydantic import BaseModel

from ...interfaces import BaseLLM


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
        self.ask_calls: list[dict] = []
        self.formatted_ask_calls: list[dict] = []

    async def prepare(self):
        await asyncio.sleep(0)

    async def ask(self, text: str, instruction: str = "") -> str:
        self.ask_calls.append({"text": text, "instruction": instruction})
        return f"dummy response for: {text}"

    async def formatted_ask(
        self,
        text: str,
        output_format: type[BaseModel],
        instruction: str = "",
    ) -> BaseModel:
        self.formatted_ask_calls.append(
            {"text": text, "output_format": output_format, "instruction": instruction}
        )
        # model_construct skips validation — intentional for speed in tests.
        return output_format.model_construct()
