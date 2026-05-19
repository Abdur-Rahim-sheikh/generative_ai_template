from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.responses import Response

from ...config import app_logger
from ...dependencies.ai_services import (
    get_chat_service,
    make_llm,
    make_tts,
    get_tts_service,
)
from ...schemas.chat import ChatRequest, ChatResponse
from ...schemas.script import ScriptRequest
from ...services import ChatService, TTSService


@asynccontextmanager
async def lifespan(app: FastAPI):
    llm = make_llm()
    tts = make_tts()
    await llm.prepare()
    app_logger.info("ollama prepared")

    await tts.load_essentials()
    app_logger.info("coqui tts prepared")

    yield


router = APIRouter(lifespan=lifespan)


@router.post("/generate-script")
async def generate_script(
    request: ChatRequest, chat_service: ChatService = Depends(get_chat_service)
) -> ChatResponse:
    wallet_id = "123e4567-e89b-12d3-a456-426614174000"
    product_id = "123e4567-e89b-12d3-a456-426614174001"
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
        return await chat_service.make_script(
            wallet_id=wallet_id,
            product_id=product_id,
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
async def generate_tts(
    request: ScriptRequest,
    tts_service: TTSService = Depends(get_tts_service),
    chat_service: ChatService = Depends(get_chat_service),
):
    wallet_id = "123e4567-e89b-12d3-a456-426614174000"
    product_id = "123e4567-e89b-12d3-a456-426614174001"
    if request.enhance_text:
        need_enhanced = [segment.text for segment in request.segments]

        try:
            response = await chat_service.enhance_script_text(
                segments=need_enhanced, language_id=request.segments[0].language_id
            )

            for i, txt in enumerate(response.enhanced_texts):
                if i < len(request.segments):
                    request.segments[i].text = txt
        except Exception as e:
            app_logger.error(msg="Failed to enhance the text", exc_info=e)

    try:
        audio = await tts_service.generate_tts(
            wallet_id=wallet_id, product_id=product_id, segments=request.segments
        )
    except Exception as e:
        msg = f"service {e}"
        raise HTTPException(status_code=400, detail=msg)

    headers = {
        "X-Enhanced-Text": str(request.enhance_text),
        "Content-Length": str(len(audio)),
        "Content-Disposition": 'attachment; filename="output.mp3"',
    }

    return Response(content=audio, media_type="audio/mp3", headers=headers)
