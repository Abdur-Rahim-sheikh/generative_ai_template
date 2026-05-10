import pytest

from ....services.tts_service import TTSService
from ....schemas.script import SpeechSegment
from ...dummies import DummyTTS


@pytest.fixture
def tts() -> DummyTTS:
    tts = DummyTTS()
    tts.available_languages = [("English", "en"), ("Bangla", "bn"), ("Arabic", "ar")]
    tts.language_codes = {"en", "bn", "ar"}
    return tts


@pytest.fixture
def service(tts) -> TTSService:
    return TTSService(tts=tts)


def make_segment(text="Hello", lang="en") -> SpeechSegment:
    return SpeechSegment(text=text, language_id=lang, gender="female", person_id=1)


class TestTTSServiceGenerate:
    async def test_generate_tts_returns_bytes(self, service):
        segments = [make_segment("Hello world", "en")]
        result = await service.generate_tts(segments)
        assert isinstance(result, bytes)
        assert len(result) > 0

    async def test_generate_tts_calls_synthesize(self, service, tts):
        segments = [make_segment("Test", "en")]
        await service.generate_tts(segments)
        assert len(tts.synthesize_calls) == 1

    async def test_generate_tts_passes_segments_to_synthesize(self, service, tts):
        segments = [make_segment("Hi", "en"), make_segment("Salam", "bn")]
        await service.generate_tts(segments)
        assert tts.synthesize_calls[0] == segments

    async def test_generate_tts_raises_for_unsupported_language(self, service):
        segments = [make_segment("Hola", "es")]
        with pytest.raises(ValueError, match="es"):
            await service.generate_tts(segments)

    async def test_error_message_lists_allowed_languages(self, service):
        segments = [make_segment("test", "zz")]
        with pytest.raises(ValueError) as exc_info:
            await service.generate_tts(segments)
        assert "zz" in str(exc_info.value)

    async def test_text_is_cleaned_before_synthesis(self, service, tts):
        """Numbers in text should be converted to words before sending to TTS."""
        segments = [make_segment("I have 3 apples", "en")]
        await service.generate_tts(segments)
        synthesized = tts.synthesize_calls[0][0]
        assert "3" not in synthesized.text
        assert "three" in synthesized.text.lower()

    async def test_multiple_segments_all_validated(self, service, tts):
        segments = [
            make_segment("Hello", "en"),
            make_segment("Salam", "bn"),
        ]
        await service.generate_tts(segments)
        assert len(tts.synthesize_calls) == 1

    async def test_first_segment_valid_second_invalid_raises(self, service):
        segments = [make_segment("Hello", "en"), make_segment("Hola", "es")]
        with pytest.raises(ValueError):
            await service.generate_tts(segments)


class TestNormalizeNumbers:
    """Unit tests for TTSService.normalize_numbers — tested directly."""

    @pytest.fixture
    def normalizer(self, service) -> TTSService:
        return service

    def test_plain_digit_converted(self, normalizer):
        result = normalizer.normalize_numbers("I have 5 cats", "en")
        assert "five" in result.lower()
        assert "5" not in result

    def test_no_digits_returns_unchanged(self, normalizer):
        text = "No numbers here"
        assert normalizer.normalize_numbers(text, "en") == text

    def test_currency_dollar_converted(self, normalizer):
        result = normalizer.normalize_numbers("Pay $10 now", "en")
        assert "10" not in result
        assert "dollar" in result.lower() or "usd" in result.lower()

    def test_year_context_converted(self, normalizer):
        result = normalizer.normalize_numbers("since 2020", "en")
        assert "2020" not in result

    def test_ordinal_converted(self, normalizer):
        result = normalizer.normalize_numbers("the 1st place winner", "en")
        assert "1st" not in result
        assert "first" in result.lower()

    def test_unsupported_lang_returns_text_unchanged(self, normalizer):
        text = "Pay 100 now"
        result = normalizer.normalize_numbers(text, "xx-invalid")
        assert result == text

    def test_extra_whitespace_is_stripped(self, normalizer):
        result = normalizer.normalize_numbers("count: 2", "en")
        assert "  " not in result
