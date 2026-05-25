from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..adapters import ComfyClient, ComfyImage, CoquiTTS, OllamaLLM
from ..config import settings
from ..config.connections import async_session_maker, get_async_session
from ..repositories import UnitOfWork
from ..services import BillingService, ChatService, ImageService, TTSService
from ..tests.dummies import DummyImageGenerator, DummyLLM, DummyTTS

_ADAPTER_CACHE: dict[str, object] = {}


def make_llm():
    if "llm" in _ADAPTER_CACHE:
        return _ADAPTER_CACHE["llm"]

    if settings.USE_DUMMY_SERVICES:
        _ADAPTER_CACHE["llm"] = DummyLLM()
    _ADAPTER_CACHE["llm"] = OllamaLLM()
    return _ADAPTER_CACHE["llm"]


def make_tts():
    if "tts" in _ADAPTER_CACHE:
        return _ADAPTER_CACHE["tts"]

    if settings.USE_DUMMY_SERVICES:
        _ADAPTER_CACHE["tts"] = DummyTTS()
    _ADAPTER_CACHE["tts"] = CoquiTTS()
    return _ADAPTER_CACHE["tts"]


def make_comfy_image() -> ComfyImage:
    if "comfy_image" in _ADAPTER_CACHE:
        return _ADAPTER_CACHE["comfy_image"]

    if settings.USE_DUMMY_SERVICES:
        _ADAPTER_CACHE["comfy_image"] = DummyImageGenerator()
    _ADAPTER_CACHE["comfy_image"] = ComfyImage(
        client=ComfyClient(host=settings.COMFY_HOST, port=settings.COMFY_PORT)
    )
    return _ADAPTER_CACHE["comfy_image"]


def make_billing_service(session: AsyncSession) -> BillingService:
    uow = UnitOfWork(session=session)
    return BillingService(uow=uow)


# Service making starts here


def make_chat_service(session: AsyncSession) -> ChatService:
    return ChatService(llm=make_llm(), billing=make_billing_service(session))


def make_tts_service(session: AsyncSession) -> TTSService:
    return TTSService(tts=make_tts(), billing=make_billing_service(session))


def make_custom_image_service(session: AsyncSession) -> ImageService:
    return ImageService(
        image_generator=make_comfy_image(),
        billing=make_billing_service(session=session),
    )


def make_premium_image_service(session: AsyncSession) -> ImageService:
    pass


def make_image_service(session: AsyncSession, premium: bool = False) -> ImageService:
    if premium:
        return make_premium_image_service(session=session)

    return make_custom_image_service(session=session)


# Finally, the dependency getters for FastAPI
def get_chat_service(session: AsyncSession = Depends(get_async_session)) -> ChatService:
    return make_chat_service(session=session)


def get_tts_service(session: AsyncSession = Depends(get_async_session)) -> TTSService:
    return make_tts_service(session=session)


# for ARQ workers


@asynccontextmanager
async def image_service_worker_ctx(
    premium: bool = False,
) -> AsyncGenerator[ImageService, None]:
    async with async_session_maker() as session:
        image_service = make_image_service(session=session, premium=premium)
        yield image_service
