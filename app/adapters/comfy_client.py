import asyncio
import json
import uuid

import aiohttp

from ..config import app_logger
from ..schemas.comfy import ComfyStatus
from ..utils.image import encode_bytes_to_base64


class ComfyClient:
    def __init__(self, host: str, port: int):
        self.url = f"http://{host}:{port}"
        self.ws_url = f"ws://{host}:{port}/ws"
        self.client_id = uuid.uuid4().hex
        self.futures: dict[str, asyncio.Future] = dict()
        self.session = None
        self.ws = None
        self._loop_task = None
        self._lock = asyncio.Lock()
        self.connected = False

    async def connect(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        if self.ws is None:
            url = f"{self.ws_url}?clientId={self.client_id}"
            try:
                self.ws = await self.session.ws_connect(url=url, heartbeat=45)
                self._loop_task = asyncio.create_task(self._ws_loop())
                app_logger.debug(f"Connected to comfyui US: {url}")
            except Exception as e:
                app_logger.exception(f"Failed to connect {e}")
                raise
            self.connected = True

    async def disconnect(self):
        if self.ws:
            await self.ws.close()
        if self._loop_task is not None:
            self._loop_task.cancel()

            try:
                await self._loop_task
            except asyncio.CancelledError:
                pass

        if self.session is not None:
            await self.session.close()

        self.ws = None
        self.session = None
        self._loop_task = None
        self.connected = False

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def _ws_loop(self):
        try:
            async for msg in self.ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    await self._handle_message(json.loads(msg.data))
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    app_logger.error(
                        f"WS connection closed with error {self.ws.exception()}"
                    )
                    break
        except asyncio.CancelledError:
            pass
        finally:
            app_logger.debug("WebSocket loop stopped")

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
        images = []

        for image_info in image_infos:
            filename = image_info["filename"]
            subfolder = image_info["subfolder"]
            img_type = image_info["type"]

            params = {"filename": filename, "subfolder": subfolder, "type": img_type}

            async with self.session.get(f"{self.url}/view", params=params) as resp:
                resp.raise_for_status()
                images.append(await resp.read())

        return images

    async def upload_image(self, image_bytes: bytes, file_name: str) -> str:
        if not self.connected:
            raise RuntimeError("Please connect the socket before action")

        data = aiohttp.FormData()

        data.add_field(
            "image", image_bytes, filename=file_name, content_type="image/png"
        )
        data.add_field("overwrite", "true")

        try:
            async with self.session.post(f"{self.url}/upload/image", data=data) as resp:
                resp.raise_for_status()
                response = await resp.json()
                return response["name"]
        except aiohttp.ClientError as e:
            app_logger.critical(f"image could not be uploaded {e}")
            raise RuntimeError("image could not be uploaded") from e

    async def __queue_prompt(self, workflow: dict) -> str:
        async with self.session.post(
            f"{self.url}/prompt", json={"prompt": workflow, "client_id": self.client_id}
        ) as resp:
            result = await resp.json()
            if "error" in result:
                raise Exception(f"ComfyUI Error: {result['error']}")

            return result["prompt_id"]

    def __cleanup(self, prompt_id: str):
        self.futures.pop(prompt_id, None)

    async def generate_image(self, workflow: dict) -> list[str]:
        if self.ws is None:
            raise RuntimeError("Connect websocket before any generation")

        prompt_id = await self.__queue_prompt(workflow=workflow)
        app_logger.debug(f"workflow queued: {prompt_id}")

        loop = asyncio.get_running_loop()
        future = loop.create_future()

        async with self._lock:
            self.futures[prompt_id] = future

        try:
            images = await asyncio.wait_for(future, timeout=900)
            images = [encode_bytes_to_base64(image) for image in images]

            return images
        except asyncio.TimeoutError as e:
            app_logger.exception(f"Timeout waiting for prompt_id: {prompt_id}")
            raise RuntimeError("timeout on job execution") from e
        finally:
            self.__cleanup(prompt_id=prompt_id)
