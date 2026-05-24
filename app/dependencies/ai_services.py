from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..adapters import ComfyClient, ComfyImage, CoquiTTS, OllamaLLM
from ..config import settings
from ..config.connections import get_async_session, async_session_maker
from ..repositories import UnitOfWork
from ..services import BillingService, ChatService, ImageService, TTSService
from ..tests.dummies import DummyLLM, DummyTTS, DummyImageGenerator


def make_llm():
    if settings.USE_DUMMY_SERVICES:
        return DummyLLM()
    return OllamaLLM()


def make_tts():
    if settings.USE_DUMMY_SERVICES:
        return DummyTTS()
    return CoquiTTS()


def make_comfy_image() -> ComfyImage:
    if settings.USE_DUMMY_SERVICES:
        return DummyImageGenerator()
    return ComfyImage(
        client=ComfyClient(host=settings.COMFY_HOST, port=settings.COMFY_PORT)
    )


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
