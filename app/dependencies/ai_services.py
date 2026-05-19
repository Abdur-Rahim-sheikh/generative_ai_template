from fastapi import Depends

from ..config import settings
from ..adapters import OllamaLLM, CoquiTTS, ComfyImage, ComfyClient
from ..tests.dummies import DummyLLM, DummyTTS

from ..services import ChatService, TTSService, ImageService, BillingService


def get_billing_service():
    return BillingService()


def get_llm():
    if settings.USE_DUMMY_SERVICES:
        return DummyLLM()
    return OllamaLLM()


def get_tts():
    if settings.USE_DUMMY_SERVICES:
        return DummyTTS()
    return CoquiTTS()


def get_comfy_image() -> ComfyImage:
    return ComfyImage(
        client=ComfyClient(host=settings.COMFY_HOST, port=settings.COMFY_PORT)
    )


def get_chat_service(llm=Depends(get_llm)):
    return ChatService(llm, billing=get_billing_service())


def get_tts_service(tts=Depends(get_tts)):
    return TTSService(tts, billing=get_billing_service())


# these are jobqueue, so removing depends methods
def get_custom_image_service() -> ImageService:
    return ImageService(
        image_generator=get_comfy_image(), billing=get_billing_service()
    )


def get_premium_image_service():
    pass


def get_image_service() -> ImageService:
    # if else block when we connect the premium one
    return get_custom_image_service()
