from typing import Annotated, Literal

from annotated_types import MinLen
from pydantic import BaseModel

# class Language(str, Enum):
#     EN = "en"  # English
#     AR = "ar"  # Arabic
#     ZH = "zh"  # Chinese
#     CS = "cs"  # Czech
#     NL = "nl"  # Dutch
#     DE = "de"  # German
#     HI = "hi"  # Hindi
#     HU = "hu"  # Hungarian
#     IT = "it"  # Italian
#     JA = "ja"  # Japanese
#     KO = "ko"  # Korean
#     PL = "pl"  # Polish
#     PT = "pt"  # Portuguese
#     RU = "ru"  # Russian
#     ES = "es"  # Spanish
#     TR = "tr"  # Turkish
#     BN = "bn"  # Bangla with bangla models


class SpeechSegment(BaseModel):
    text: str
    language_id: str
    gender: Literal["female", "male"]
    person_id: Literal[1, 2]


class BaseScript(BaseModel):
    segments: Annotated[list[SpeechSegment], MinLen(min_length=1)]


class ScriptRequest(BaseScript):
    enhance_text: bool
