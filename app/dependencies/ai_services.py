from fastapi import Depends

from ..config import settings
from ..adapters import OllamaLLM, CoquiTTS
from ..tests.dummies import DummyLLM, DummyTTS

from ..services import ChatService, TTSService


def get_llm():
    if settings.USE_DUMMY_SERVICES:
        return DummyLLM()
    return OllamaLLM()


def get_tts():
    if settings.USE_DUMMY_SERVICES:
        return DummyTTS()
    return CoquiTTS()


def get_chat_service(llm=Depends(get_llm)):
    return ChatService(llm)


def get_tts_service(tts=Depends(get_tts)):
    return TTSService(tts)
