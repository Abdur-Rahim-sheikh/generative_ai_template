import base64
from io import BytesIO

from fastapi import HTTPException, status
from PIL import Image


def encode_image_to_base64(image: Image.Image) -> str:
    buffer = BytesIO()
    image.save(buffer, format="png")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def encode_bytes_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def decode_base64_to_image(b64: str) -> Image.Image:
    try:
        return Image.open(BytesIO(base64.b64decode(b64, validate=True))).convert("RGB")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image url"
        ) from e


def decode_base64_to_bytes(b64: str) -> bytes:
    try:
        return base64.b64decode(b64, validate=True)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid base64 string"
        ) from e
