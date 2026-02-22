from fastapi import APIRouter

from ..config import settings
from ..data import CoquiTTS

coqui_tts = CoquiTTS(host=settings.COQUI_HOST, port=settings.COQUI_PORT)
router = APIRouter()


@router.get("/internal-supported-languages")
async def coqui_languages() -> list[tuple[str, str]]:
    return await coqui_tts.allowed_languages()
