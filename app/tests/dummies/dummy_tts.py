import asyncio


from ...config import app_logger
from ...interfaces import BaseTTS
from ...schemas.script import SpeechSegment


class DummyTTS(BaseTTS):
    def __init__(self):
        self.available_languages: list = []
        self.language_codes: set = set()

    async def load_essentials(self):
        await asyncio.sleep(0.5)
        self.available_languages = [("Abir", "ab"), ("Nadia", "nd")]
        self.language_codes = set({lang[-1] for lang in self.available_languages})

    def has_language(self, language_code: str) -> bool:
        return language_code in self.language_codes

    async def allowed_languages(self) -> list[tuple[str, str]]:
        if not self.available_languages:
            await self.load_essentials()

        return self.available_languages

    async def synthesize(self, segments: list[SpeechSegment]) -> bytes:
        turns = [
            {
                "text": segment.text,
                "language_id": segment.language_id,
                "gender": segment.gender,
                "person_id": segment.person_id,
            }
            for segment in segments
        ]
        request = {"turns": turns, "stitch_delay": 0.5}

        await asyncio.sleep(0.3 * len(turns))
        app_logger.debug(f"Dummy tts received: {request}")
        return b"dummy bytes audio"
