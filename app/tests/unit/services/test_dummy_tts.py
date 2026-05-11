
from ...dummies import DummyTTS
from ....interfaces import BaseTTS
from ....schemas.script import SpeechSegment


def seg(text="Hi", lang="en") -> SpeechSegment:
    return SpeechSegment(text=text, language_id=lang, gender="female", person_id=1)


class TestDummyTTS:
    def test_dummy_tts_is_base_tts_subclass(self):
        assert issubclass(DummyTTS, BaseTTS)

    async def test_allowed_languages_returns_list(self):
        tts = DummyTTS()
        langs = await tts.allowed_languages()
        assert isinstance(langs, list)
        assert len(langs) > 0

    async def test_has_language_true_for_loaded_lang(self):
        tts = DummyTTS()
        await tts.load_essentials()
        assert tts.has_language("en") is True

    async def test_has_language_false_for_unknown_lang(self):
        tts = DummyTTS()
        await tts.load_essentials()
        assert tts.has_language("xx-fake") is False

    async def test_synthesize_returns_bytes(self):
        tts = DummyTTS()
        await tts.load_essentials()
        result = await tts.synthesize([seg()])
        assert isinstance(result, bytes)
        assert len(result) > 0

    async def test_synthesize_records_call(self):
        tts = DummyTTS()
        segments = [seg("Hello"), seg("World")]
        await tts.synthesize(segments)
        assert len(tts.synthesize_calls) == 1

    async def test_allowed_languages_lazy_loads(self):
        tts = DummyTTS()
        assert tts.available_languages == []
        langs = await tts.allowed_languages()
        assert len(langs) > 0

    async def test_instances_are_independent(self):
        tts1 = DummyTTS()
        tts2 = DummyTTS()
        await tts1.synthesize([seg()])
        assert len(tts1.synthesize_calls) == 1
        assert len(tts2.synthesize_calls) == 0
