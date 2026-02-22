import logging
import os
import tempfile
from contextlib import asynccontextmanager
from io import BytesIO
from pathlib import Path

import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse, Response
from iso639 import Language as IsoLang
from pedalboard import Compressor, HighpassFilter, Pedalboard, Reverb
from pydub import AudioSegment
from TTS.api import TTS
from tts_schemas import Language, RequestSchema, get_speaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


OUTPUT_FOLDER = Path("temp_audio")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

tts = None
bn_tts: dict[str, TTS] = {}


@asynccontextmanager
async def lifespan(_app: FastAPI):
    global tts
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device="cuda")
    await load_bangla_model()
    logger.info("xtts_v2 model loaded")
    yield


async def load_bangla_model():
    global bn_tts
    bn_tts["male"] = TTS("tts_models/bn/custom/vits-male").to(device="cuda")
    bn_tts["female"] = TTS("tts_models/bn/custom/vits-female").to(device="cuda")
    logger.info("bangla custom model loaded")


app = FastAPI(title="Coqui-tts server", lifespan=lifespan)


@app.get("/speakers")
def get_speakers():
    return {"speakers": tts.speakers}


@app.get("/models")
def get_models():
    return {"models": tts.list_models()}


def apply_mastering(segment: AudioSegment):
    samples = np.array(segment.get_array_of_samples()).astype(np.float32) / 32768
    board = Pedalboard(
        [
            HighpassFilter(cutoff_frequency_hz=80),
            Compressor(threshold_db=-18, ratio=2.5),
            Reverb(room_size=0.1, dry_level=0.95, wet_level=0.05),
        ]
    )
    mastered = board(samples, segment.frame_rate)
    mastered /= np.max(np.abs(mastered))
    mastered_int = (mastered * 32767).astype(np.int16)
    return AudioSegment(
        mastered_int.tobytes(),
        frame_rate=segment.frame_rate,
        sample_width=2,
        channels=1,
    )


@app.get("/available_languages")
async def available_languages() -> JSONResponse:
    response = []
    for lang_id in Language:
        lang_id = lang_id.value
        try:
            lang = IsoLang.from_part1(lang_id)
        except Exception:
            continue
        response.append((lang.name, lang_id))
    return JSONResponse(content=response)


@app.post("/generate")
async def generate_audio(request: RequestSchema):
    GAP = AudioSegment.silent(duration=int(request.stich_delay * 1000))
    temp_files = []
    try:
        combined = GAP
        for turn in request.turns:
            fd, path = tempfile.mkstemp(suffix=".wav", dir=OUTPUT_FOLDER)
            os.close(fd)

            temp_files.append(path)

            if turn.language_id.value == "bn":
                bn_tts[turn.gender].tts_to_file(
                    text=turn.text,
                    file_path=path,
                    temperature=0.65,
                    top_p=0.8,
                    length_penalty=1.0,
                    repetition_penalty=10.0,
                    speed=1.05,
                    enable_text_splitting=True,
                )
            else:
                speaker = get_speaker(
                    language_code=turn.language_id.value,
                    gender=turn.gender,
                    person_id=turn.person_id,
                )
                logger.debug(f"{speaker=}")

                tts.tts_to_file(
                    text=turn.text,
                    speaker=speaker,
                    language=turn.language_id.value,
                    file_path=path,
                    temperature=0.75,
                    top_p=0.85,
                    length_penalty=1.0,
                    repetition_penalty=5.0,
                    speed=1.05,
                    enable_text_splitting=True,
                )
            part = AudioSegment.from_wav(file=path)

            combined += part + GAP

        # post processing
        combined = apply_mastering(combined)
        output_buffer = BytesIO()
        combined.export(output_buffer, format="mp3", bitrate="192k")
        output_buffer.seek(0)

        content = output_buffer.getvalue()
        return Response(
            content=content,
            media_type="audio/mp3",
            headers={
                "Content-Length": str(len(content)),
                "Content-Disposition": 'attachment; filename="output.mp3"',
            },
        )
    except Exception as e:
        logger.error(f"Error {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        for f in temp_files:
            Path(f).unlink(missing_ok=True)


@app.post("/mimic")
async def mimic(
    text: str = Form(...), language: str = Form("en"), file: UploadFile = File(...)
):
    # need to install torchcodec
    ref_path = None
    out_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".wav", dir=OUTPUT_FOLDER
        ) as temp:
            content = await file.read()
            temp.write(content)
            ref_path = temp.name

        fd, out_path = tempfile.mkstemp(suffix=".wav", dir=OUTPUT_FOLDER)
        os.close(fd)

        tts.tts(text=text, speaker_wav=ref_path, language=language, file_path=out_path)

        with open(out_path, "rb") as file:
            data = file.read()

        return Response(BytesIO(data).getvalue(), media_type="audio/wav")

    except Exception as e:
        logger.error(f"Mimicking error {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if ref_path:
            Path(ref_path).unlink(missing_ok=True)
        if out_path:
            Path(out_path).unlink(missing_ok=True)


@app.get("/healthcheck", status_code=200)
def healthcheck():
    return "OK"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8020)
