from pydantic import BaseModel

from ...dummies import DummyLLM
from ....interfaces import BaseLLM


class SampleOutput(BaseModel):
    message: str = "default"
    count: int = 0


class TestDummyLLM:
    def test_dummy_llm_is_base_llm_subclass(self):
        assert issubclass(DummyLLM, BaseLLM)

    async def test_ask_returns_string(self):
        llm = DummyLLM()
        result = await llm.ask("hello")
        assert isinstance(result, str)

    async def test_ask_records_call(self):
        llm = DummyLLM()
        await llm.ask("prompt", instruction="sys")
        assert len(llm.ask_calls) == 1
        assert llm.ask_calls[0]["text"] == "prompt"
        assert llm.ask_calls[0]["instruction"] == "sys"

    async def test_ask_default_instruction_is_empty(self):
        llm = DummyLLM()
        await llm.ask("test")
        assert llm.ask_calls[0]["instruction"] == ""

    async def test_formatted_ask_returns_instance_of_output_format(self):
        llm = DummyLLM()
        result = await llm.formatted_ask("text", SampleOutput)
        assert isinstance(result, SampleOutput)

    async def test_formatted_ask_records_call(self):
        llm = DummyLLM()
        await llm.formatted_ask("text", SampleOutput, instruction="sys")
        assert len(llm.formatted_ask_calls) == 1
        call = llm.formatted_ask_calls[0]
        assert call["output_format"] is SampleOutput
        assert call["instruction"] == "sys"

    async def test_instances_are_independent(self):
        """Each DummyLLM instance must have its own call history."""
        llm1 = DummyLLM()
        llm2 = DummyLLM()
        await llm1.ask("a")
        assert len(llm1.ask_calls) == 1
        assert len(llm2.ask_calls) == 0
