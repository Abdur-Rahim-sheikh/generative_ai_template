import re

from num2words import num2words

from ..config import app_logger
from ..interfaces import BaseTTS
from ..schemas.script import SpeechSegment


class TTSService:
    CURRENCY_MAP = {"$": "USD", "৳": "BDT", "€": "EUR"}
    CURRENCY_RE = re.compile(r"([\$£€৳₹])\s?(\d+\.?\d*)")
    YEAR_RE = re.compile(
        r"\b(in|since|year|dated|from|to|between)\b\s+(\d{4})\b", re.IGNORECASE
    )
    ORDINAL_SUFFIX_RE = re.compile(r"\b(\d+)(st|nd|rd|th)\b")
    STANDALONE_DIGIT_RE = re.compile(r"\b\d+\b")

    def __init__(self, tts: BaseTTS):
        self.tts = tts

    def normalize_numbers(self, text: str, lang: str):
        try:
            num2words("1", lang=lang)
        except NotImplementedError:
            return text
        if not re.search(r"\d", text):
            return text
        # currency handler

        text = self.CURRENCY_RE.sub(
            lambda m: num2words(
                float(m.group(2)),
                lang=lang,
                to="currency",
                currency=self.CURRENCY_MAP.get(m.group(1), "USD"),
            ),
            text,
        )

        # year handler

        def __year_repl(m: re.Match):
            prefix = m.group(1)
            number = m.group(2)
            return f"{prefix} {num2words(int(number), lang=lang, to='year')}"

        text = self.YEAR_RE.sub(__year_repl, text)

        # ordinals (1st, 2nd)
        text = self.ORDINAL_SUFFIX_RE.sub(
            lambda m: num2words(int(m.group(1)), lang=lang, to="ordinal"),
            text,
        )

        # ordinals
        text = self.STANDALONE_DIGIT_RE.sub(
            lambda m: num2words(int(m.group()), lang=lang), text
        )
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def clean_text(self, text: str, lang: str) -> str:
        # step1 normalize numbers
        result = self.normalize_numbers(text, lang=lang)
        return result

    async def generate_tts(self, segments: list[SpeechSegment]) -> bytes:
        for idx, segment in enumerate(segments):
            if not self.tts.has_language(segment.language_id):
                raise ValueError(
                    f"Language {segment.language_id} is not be within {await self.tts.allowed_languages()}"
                )
            app_logger.debug(f"Cleaned, {segment.text} in {segment.language_id=}")
            segments[idx].text = self.clean_text(segment.text, segment.language_id)
            app_logger.debug(f" to {segments[idx].text}")
        return await self.tts.synthesize(segments=segments)
