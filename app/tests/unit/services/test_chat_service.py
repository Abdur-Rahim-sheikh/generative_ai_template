import pytest

from ....services.chat_service import ChatService
from ....schemas.chat import ChatResponse, EnhancedTextList
from ...dummies import DummyLLM


@pytest.fixture
def llm() -> DummyLLM:
    return DummyLLM()


@pytest.fixture
def service(llm) -> ChatService:
    return ChatService(llm=llm)


class TestChatServiceMonologue:
    async def test_make_script_monologue_returns_chat_response(self, service):
        response = await service.make_script(
            product="SuperApp",
            goal="increase downloads",
            audience="millennials",
            platform="Instagram",
            tone="energetic",
            language="en",
            duration="short",
            format="monologue",
        )
        assert isinstance(response, ChatResponse)

    async def test_make_script_monologue_has_single_dialogue_entry(self, service):
        response = await service.make_script(
            product="X",
            goal="Y",
            audience="Z",
            platform="W",
            tone="casual",
            language="en",
            duration="short",
            format="monologue",
        )
        assert len(response.dialogue) == 1

    async def test_make_script_monologue_uses_llm_ask(self, service, llm):
        await service.make_script(
            product="X",
            goal="Y",
            audience="Z",
            platform="W",
            tone="casual",
            language="en",
            duration="short",
            format="monologue",
        )
        assert len(llm.ask_calls) == 1
        assert len(llm.formatted_ask_calls) == 0

    async def test_monologue_system_prompt_is_sent(self, service, llm):
        await service.make_script(
            product="X",
            goal="Y",
            audience="Z",
            platform="W",
            tone="casual",
            language="en",
            duration="short",
            format="monologue",
        )
        call = llm.ask_calls[0]
        assert "monologue" in call["instruction"].lower()

    async def test_monologue_text_contains_product(self, service, llm):
        await service.make_script(
            product="MyCoolProduct",
            goal="Y",
            audience="Z",
            platform="W",
            tone="casual",
            language="en",
            duration="short",
            format="monologue",
        )
        assert "MyCoolProduct" in llm.ask_calls[0]["text"]

    async def test_monologue_gender_is_female(self, service):
        response = await service.make_script(
            product="X",
            goal="Y",
            audience="Z",
            platform="W",
            tone="casual",
            language="en",
            duration="short",
            format="monologue",
        )
        assert response.dialogue[0].gender == "female"

    async def test_monologue_person_id_is_1(self, service):
        response = await service.make_script(
            product="X",
            goal="Y",
            audience="Z",
            platform="W",
            tone="casual",
            language="en",
            duration="short",
            format="monologue",
        )
        assert response.dialogue[0].person_id == 1


class TestChatServiceDialogue:
    async def test_make_script_dialogue_returns_chat_response(self, service):
        response = await service.make_script(
            product="X",
            goal="Y",
            audience="Z",
            platform="W",
            tone="casual",
            language="en",
            duration="short",
            format="dialogue",
        )
        assert isinstance(response, ChatResponse)

    async def test_make_script_dialogue_uses_formatted_ask(self, service, llm):
        await service.make_script(
            product="X",
            goal="Y",
            audience="Z",
            platform="W",
            tone="casual",
            language="en",
            duration="short",
            format="dialogue",
        )
        assert len(llm.formatted_ask_calls) == 1
        assert len(llm.ask_calls) == 0

    async def test_dialogue_output_format_is_chat_response(self, service, llm):
        await service.make_script(
            product="X",
            goal="Y",
            audience="Z",
            platform="W",
            tone="casual",
            language="en",
            duration="short",
            format="dialogue",
        )
        call = llm.formatted_ask_calls[0]
        assert call["output_format"] is ChatResponse

    async def test_dialogue_system_prompt_is_sent(self, service, llm):
        await service.make_script(
            product="X",
            goal="Y",
            audience="Z",
            platform="W",
            tone="casual",
            language="en",
            duration="short",
            format="dialogue",
        )
        call = llm.formatted_ask_calls[0]
        assert "dialogue" in call["instruction"].lower()


class TestEnhanceScriptText:
    async def test_enhance_returns_enhanced_text_list(self, service):
        result = await service.enhance_script_text(
            segments=["Buy now!", "Limited offer."],
            language_id="en",
        )
        assert isinstance(result, EnhancedTextList)

    async def test_enhance_uses_formatted_ask(self, service, llm):
        await service.enhance_script_text(segments=["Hello world"], language_id="en")
        assert len(llm.formatted_ask_calls) == 1

    async def test_enhance_system_prompt_contains_segment_count(self, service, llm):
        segs = ["Line one", "Line two", "Line three"]
        await service.enhance_script_text(segments=segs, language_id="en")
        instruction = llm.formatted_ask_calls[0]["instruction"]
        assert str(len(segs)) in instruction

    async def test_enhance_numbered_lines_in_text(self, service, llm):
        segs = ["Alpha", "Beta"]
        await service.enhance_script_text(segments=segs, language_id="en")
        text = llm.formatted_ask_calls[0]["text"]
        assert "1. Alpha" in text
        assert "2. Beta" in text


class TestEnhanceImagePrompt:
    async def test_enhance_prompt_returns_string(self, service):
        result = await service.enhance_realistic_image_prompt("a cat on a table")
        assert isinstance(result, str)

    async def test_enhance_prompt_uses_llm_ask(self, service, llm):
        await service.enhance_realistic_image_prompt("a dog in the park")
        assert len(llm.ask_calls) == 1

    async def test_enhance_prompt_sends_original_text(self, service, llm):
        await service.enhance_realistic_image_prompt("sunset over the ocean")
        assert "sunset over the ocean" in llm.ask_calls[0]["text"]
