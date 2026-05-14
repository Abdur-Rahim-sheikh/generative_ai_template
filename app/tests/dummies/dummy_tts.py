import asyncio

from ...interfaces import BaseTTS
from ...schemas.script import SpeechSegment


class DummyTTS(BaseTTS):
    """
    In-process TTS double.

    Simulates a small language list and returns deterministic bytes so
    tests never need a real TTS server.
    """

    _DEFAULT_LANGUAGES = [("English", "en"), ("Bangla", "bn"), ("Arabic", "ar")]

    def __init__(self):
        self.available_languages: list[tuple[str, str]] = []
        self.language_codes: set[str] = set()
        self.synthesize_calls: list[list[SpeechSegment]] = []

    async def load_essentials(self):
        await asyncio.sleep(0)
        self.available_languages = list(self._DEFAULT_LANGUAGES)
        self.language_codes = {lang[1] for lang in self.available_languages}

    def has_language(self, language_code: str) -> bool:
        return language_code in self.language_codes

    async def allowed_languages(self) -> list[tuple[str, str]]:
        if not self.available_languages:
            await self.load_essentials()
        return self.available_languages

    async def synthesize(self, segments: list[SpeechSegment]) -> bytes:
        self.synthesize_calls.append(segments)
        return b"dummy audio bytes"
