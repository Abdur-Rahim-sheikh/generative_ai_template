from fastapi import APIRouter

from ..config import settings
from ..data import CoquiTTS
from ..data.dummies import DummyTTS

dummy_tts = DummyTTS()
coqui_tts = CoquiTTS(host=settings.COQUI_HOST, port=settings.COQUI_PORT)
router = APIRouter()
tts = dummy_tts if settings.USE_DUMMY_SERVICES else coqui_tts


@router.get("/internal-supported-languages")
async def coqui_languages() -> list[tuple[str, str]]:
    return await tts.allowed_languages()
