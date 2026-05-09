import asyncio
import uuid

from ...config import app_logger
from ...schemas.comfy import ComfyStatus


class DummyComfyClient:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        await asyncio.sleep(0.5)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.sleep(0.5)

    async def _handle_message(self, message: dict):
        msg_type = message.get("type")
        data: dict = message.get("data", {})
        prompt_id: str = data.get("prompt_id", "")

        if not prompt_id or prompt_id not in self.futures:
            return

        future = self.futures[prompt_id]
        if future.done():
            return

        elif msg_type == ComfyStatus.EXECUTED:
            output = data.get("output")
            if not output or "images" not in output:
                app_logger.info(
                    f"Ignored 'executed' message with no images. Node ID: {data.get('node')}"
                )
                return

            try:
                output_images = await self.get_images(image_infos=output["images"])
                future.set_result(output_images)
            except Exception as e:
                app_logger.critical(f"Failed to process images: {e}")
                future.set_exception(e)

        elif msg_type == ComfyStatus.EXECUTION_ERROR:
            node_id = data.get("node_id", "unknown node id")
            exc_msg = data.get("exception_message", "unknow exception_message")
            error_msg = f"Workflow failed: Node {node_id} for error {exc_msg}"
            app_logger.exception(msg=error_msg, exc_info=error_msg)

            future.set_exception(Exception(f"Comfyui error: {error_msg}"))

    async def get_images(self, image_infos: list[dict]) -> list[bytes]:
        images = [b"dummy image"]

        return images

    async def upload_image(self, image_bytes: bytes, file_name: str) -> str:
        await asyncio.sleep(0.5)

    async def __queue_prompt(self, workflow: dict) -> str:
        return uuid.uuid4().hex

    async def generate_image(self, workflow: dict) -> list[str]:
        prompt_id = await self.__queue_prompt(workflow=workflow)
        app_logger.debug(f"workflow queued: {prompt_id}")

        try:
            images = await self.get_images(image_infos={"ulala": "ulala"})
            images = ["base64_dummy_encoding"]

            return images
        except asyncio.TimeoutError as e:
            app_logger.exception(f"Timeout waiting for prompt_id: {prompt_id}")
            raise RuntimeError("timeout on job execution") from e
