from fastapi import APIRouter

from ...adapters import CoquiTTS
from ...config import ProductTitle, settings
from ...tests.dummies import DummyTTS

dummy_tts = DummyTTS()
coqui_tts = CoquiTTS(host=settings.COQUI_HOST, port=settings.COQUI_PORT)
router = APIRouter()
tts = dummy_tts if settings.USE_DUMMY_SERVICES else coqui_tts


@router.get("/internal-supported-languages")
async def coqui_languages() -> list[tuple[str, str]]:
    return await tts.allowed_languages()


@router.post("/setup-dummy-data")
async def setup_dummy_data():
    import aiohttp

    async with aiohttp.ClientSession() as session:
        try:
            await session.post(
                "http://localhost:8000/api/db/create-user",
                json={
                    "first_name": "Test",
                    "last_name": "User",
                    "email": "user@example.com",
                    "password": "password123",
                },
            )
        except Exception:
            pass

        for title in ProductTitle():
            try:
                await session.post(
                    "http://localhost:8000/api/db/create-product",
                    json={
                        "title": title,
                        "description": f"This is a description for {title}.",
                        "coin_cost": 1,
                    },
                )
            except Exception:
                pass

        return {"message": "Dummy entries added to the database, go check, apis now!"}
