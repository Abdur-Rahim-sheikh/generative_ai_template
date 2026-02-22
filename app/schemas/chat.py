from typing import Annotated, Literal

from annotated_types import MinLen
from pydantic import BaseModel, field_validator


class BaseChat(BaseModel):
    product: str
    goal: str
    audience: str
    platform: str
    tone: str
    language: str
    duration: Literal["short", "medium", "long"]
    forbid: str = ""


class ChatRequest(BaseChat):
    format: Literal["monologue", "dialogue"]

    @field_validator("duration", "format", mode="before", check_fields=False)
    @classmethod
    def normalize_duration(cls, v: str):
        return v.lower()


class BaseInformation(BaseModel):
    gender: Literal["male", "female"]
    text: str
    person_id: Literal[1, 2]


class ChatResponse(BaseModel):
    dialogue: Annotated[list[BaseInformation], MinLen(1)]


class EnhancedTextList(BaseModel):
    enhanced_texts: list[str]
