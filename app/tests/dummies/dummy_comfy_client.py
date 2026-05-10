import asyncio
import uuid

from ...schemas.comfy import ComfyStatus


class DummyComfyClient:
    """
    In-process Stable Diffusion / ComfyUI double.

    Never opens a network socket; returns hard-coded base64 strings so
    tests can run fully offline.
    """

    def __init__(self, *args, **kwargs):
        self.generate_calls: list[dict] = []

    async def __aenter__(self):
        await asyncio.sleep(0)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.sleep(0)

    async def get_images(self, image_infos) -> list[bytes]:
        return [b"dummy image bytes"]

    async def upload_image(self, image_bytes: bytes, file_name: str) -> str:
        await asyncio.sleep(0)
        return f"uploaded://{file_name}"

    async def _DummyComfyClient__queue_prompt(self, workflow: dict) -> str:
        return uuid.uuid4().hex

    async def generate_image(self, workflow: dict) -> list[str]:
        self.generate_calls.append(workflow)
        prompt_id = uuid.uuid4().hex
        try:
            return ["base64_dummy_encoding"]
        except asyncio.TimeoutError as e:
            raise RuntimeError("timeout on job execution") from e
