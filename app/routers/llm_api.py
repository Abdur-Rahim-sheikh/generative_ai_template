from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, HTTPException, status
from fastapi.responses import Response

from ..config import app_logger, settings
from ..data import CoquiTTS, OllamaLLM
from ..tests.dummies import DummyLLM, DummyTTS
from ..schemas.chat import ChatRequest, ChatResponse
from ..schemas.script import ScriptRequest
from ..services import ChatService, TTSService

dummy_llm = DummyLLM()
ollama_llm = OllamaLLM(host=settings.OLLAMA_HOST, model=settings.OLLAMA_MODEL)
llm = dummy_llm if settings.USE_DUMMY_SERVICES else ollama_llm


dummy_tts = DummyTTS()
coqui_tts = CoquiTTS(host=settings.COQUI_HOST, port=settings.COQUI_PORT)
tts = dummy_tts if settings.USE_DUMMY_SERVICES else coqui_tts


@asynccontextmanager
async def lifespan(app: FastAPI):
    await llm.prepare()
    app_logger.info("ollama prepared")

    await tts.load_essentials()
    app_logger.info("coqui tts prepared")

    yield


router = APIRouter(lifespan=lifespan)

chat_service_ollama = ChatService(llm=llm)

tts_service_coqui = TTSService(tts=tts)


@router.post("/generate-script")
async def generate_script(request: ChatRequest) -> ChatResponse:
    current_chat_service = chat_service_ollama

    words = 40  # if short
    if request.duration == "medium":
        words = 60
    elif request.duration == "long":
        words = 80

    duration = f"{words=} only"
    if request.format == "dialogue":
        turns = words // 10
        duration += f", within {turns=}"

    try:
        return await current_chat_service.make_script(
            product=request.product,
            goal=request.goal,
            audience=request.audience,
            platform=request.platform,
            tone=request.tone,
            language=request.language,
            duration=duration,
            forbid=request.forbid,
            format=request.format,
        )
    except RuntimeError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="llm is down",
        )


@router.post("/generate-tts")
async def generate_tts(request: ScriptRequest):
    current_tts_service = tts_service_coqui
    current_enhance_service = chat_service_ollama

    if request.enhance_text:
        need_enhanced = [segment.text for segment in request.segments]

        try:
            response = await current_enhance_service.enhance_script_text(
                segments=need_enhanced, language_id=request.segments[0].language_id
            )

            for i, txt in enumerate(response.enhanced_texts):
                if i < len(request.segments):
                    request.segments[i].text = txt
        except Exception as e:
            app_logger.error(msg="Failed to enhance the text", exc_info=e)

    try:
        audio = await current_tts_service.generate_tts(segments=request.segments)
    except Exception as e:
        msg = f"service {e}"
        raise HTTPException(status_code=400, detail=msg)

    headers = {
        "X-Enhanced-Text": str(request.enhance_text),
        "Content-Length": str(len(audio)),
        "Content-Disposition": 'attachment; filename="output.mp3"',
    }

    return Response(content=audio, media_type="audio/mp3", headers=headers)
