import httpx

from ..config import app_logger
from ..interfaces import BaseTTS
from ..schemas.script import SpeechSegment


class CoquiTTS(BaseTTS):
    def __init__(self, host: str, port: int, timeout: int = 120):
        self.url = f"http://{host}:{port}"
        timeout = httpx.Timeout(connect=5, read=timeout, write=30, pool=5)
        self.client = httpx.AsyncClient(timeout=timeout, base_url=self.url)
        self.available_languages: list = []
        self.language_codes: set = set()

    async def load_essentials(self):
        resp = await self.client.get(f"{self.url}/available_languages")
        if resp.status_code != 200:
            raise RuntimeError(f"Failse with status: {resp.status_code}")

        self.available_languages = resp.json()
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
        try:
            resp = await self.client.post(url="/generate", json=request)
            if resp.status_code != 200:
                raise
            return resp.content
        except httpx.HTTPError as e:
            app_logger.exception("coqui tts request error")
            raise e
