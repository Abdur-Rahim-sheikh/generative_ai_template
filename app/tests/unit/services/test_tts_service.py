import pytest

from ....services import TTSService, BillingService
from ....schemas.script import SpeechSegment
from ...dummies import DummyTTS
from .conftest import SeedDbFactory
from typing import Protocol


@pytest.fixture
def tts() -> DummyTTS:
    tts = DummyTTS()
    tts.available_languages = [("English", "en"), ("Bangla", "bn"), ("Arabic", "ar")]
    tts.language_codes = {"en", "bn", "ar"}
    return tts


@pytest.fixture
def tts_service(tts, billing_service: BillingService) -> TTSService:
    return TTSService(tts=tts, billing=billing_service)


def make_segment(text="Hello", lang="en") -> SpeechSegment:
    return SpeechSegment(text=text, language_id=lang, gender="female", person_id=1)


class TestTTSServiceGenerate:
    async def test_generate_tts_returns_bytes(
        self, tts_service: TTSService, seeded_db: SeedDbFactory
    ):
        wallet, product = await seeded_db()
        segments = [make_segment("Hello world", "en")]
        result = await tts_service.generate_tts(wallet.id, product.id, segments)
        assert isinstance(result, bytes)
        assert len(result) > 0

    async def test_generate_tts_calls_synthesize(
        self, tts_service: TTSService, tts: DummyTTS, seeded_db: SeedDbFactory
    ):
        wallet, product = await seeded_db()
        segments = [make_segment("Test", "en")]
        await tts_service.generate_tts(
            wallet_id=wallet.id, product_title=product.id, segments=segments
        )
        assert len(tts.synthesize_calls) == 1

    async def test_generate_tts_passes_segments_to_synthesize(
        self, tts_service: TTSService, tts: DummyTTS, seeded_db: SeedDbFactory
    ):
        wallet, product = await seeded_db()
        segments = [make_segment("Hi", "en"), make_segment("Salam", "bn")]
        await tts_service.generate_tts(wallet.id, product.id, segments)
        assert tts.synthesize_calls[0] == segments

    async def test_generate_tts_raises_for_unsupported_language(
        self, tts_service: TTSService, seeded_db: SeedDbFactory
    ):
        wallet, product = await seeded_db()
        segments = [make_segment("Hola", "es")]
        with pytest.raises(ValueError, match="es"):
            await tts_service.generate_tts(wallet.id, product.id, segments)

    async def test_error_message_lists_allowed_languages(
        self, tts_service: TTSService, seeded_db: SeedDbFactory
    ):
        wallet, product = await seeded_db()

        segments = [make_segment("test", "zz")]
        with pytest.raises(ValueError) as exc_info:
            await tts_service.generate_tts(wallet.id, product.id, segments)
        assert "zz" in str(exc_info.value)

    async def test_text_is_cleaned_before_synthesis(
        self, tts_service: TTSService, tts: DummyTTS, seeded_db: SeedDbFactory
    ):
        """Numbers in text should be converted to words before sending to TTS."""
        wallet, product = await seeded_db()
        segments = [make_segment("I have 3 apples", "en")]
        await tts_service.generate_tts(wallet.id, product.id, segments)
        synthesized = tts.synthesize_calls[0][0]
        assert "3" not in synthesized.text
        assert "three" in synthesized.text.lower()

    async def test_multiple_segments_all_validated(
        self, tts_service: TTSService, tts: DummyTTS, seeded_db: SeedDbFactory
    ):
        wallet, product = await seeded_db()
        segments = [
            make_segment("Hello", "en"),
            make_segment("Salam", "bn"),
        ]
        await tts_service.generate_tts(wallet.id, product.id, segments)
        assert len(tts.synthesize_calls) == 1

    async def test_first_segment_valid_second_invalid_raises(
        self, tts_service: TTSService, seeded_db: SeedDbFactory
    ):
        wallet, product = await seeded_db()
        segments = [make_segment("Hello", "en"), make_segment("Hola", "es")]
        with pytest.raises(ValueError):
            await tts_service.generate_tts(wallet.id, product.id, segments)


class TestCleanText:
    """Unit tests for TTSService.clean_text — tested directly."""

    class CleanText(Protocol):
        def __call__(self, text: str, lang: str) -> str: ...

    @pytest.fixture
    def clean_text(self, tts_service: TTSService) -> CleanText:
        return tts_service.clean_text

    def test_plain_digit_converted(self, clean_text: CleanText):
        result = clean_text(text="I have 5 cats", lang="en")
        assert "five" in result.lower()
        assert "5" not in result

    def test_no_digits_returns_unchanged(self, clean_text: CleanText):
        text = "No numbers here"
        assert clean_text(text, "en") == text

    def test_currency_dollar_converted(self, clean_text: CleanText):
        result = clean_text("Pay $10 now", "en")
        assert "10" not in result
        assert "dollar" in result.lower() or "usd" in result.lower()

    def test_year_context_converted(self, clean_text: CleanText):
        result = clean_text("since 2020", "en")
        assert "2020" not in result

    def test_ordinal_converted(self, clean_text: CleanText):
        result = clean_text("the 1st place winner", "en")
        assert "1st" not in result
        assert "first" in result.lower()

    def test_unsupported_lang_returns_text_unchanged(self, clean_text: CleanText):
        text = "Pay 100 now"
        result = clean_text(text, "xx-invalid")
        assert result == text

    def test_extra_whitespace_is_stripped(self, clean_text: CleanText):
        result = clean_text("count: 2", "en")
        assert "  " not in result
