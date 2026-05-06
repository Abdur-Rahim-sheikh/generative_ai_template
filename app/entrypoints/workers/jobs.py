import uuid

from ...config import app_logger, settings
from ...data import ComfyClient
from ...tests.dummies import DummyComfyClient
from ...services import WorkflowGenerator

generator = WorkflowGenerator()
Client = DummyComfyClient if settings.USE_DUMMY_SERVICES else ComfyClient


async def realistic_image(
    ctx, prompt: str, width: int, height: int, batch: int = 1
) -> bytes:
    app_logger.debug(msg=f"enhanced: {prompt=}")
    async with Client(host=settings.COMFY_HOST, port=settings.COMFY_PORT) as client:
        workflow = generator.get_realistic_image_workflow(
            prompt=prompt, width=width, height=height, batch=batch
        )
        images = await client.generate_image(workflow=workflow)
        # currently return only one due to business reason
        return images


async def product_photography(
    ctx,
    reference_image: bytes,
    prompt: str,
    width: int,
    height: int,
    batch: int = 1,
) -> bytes:
    image_name = uuid.uuid4().hex[:16]

    async with Client(host=settings.COMFY_HOST, port=settings.COMFY_PORT) as client:
        uploaded_img_name = await client.upload_image(
            image_bytes=reference_image, file_name=image_name
        )
        app_logger.debug("Image uploaded")
        workflow = generator.get_product_image_workflow(
            reference_image_name=uploaded_img_name,
            prompt=prompt,
            width=width,
            height=height,
            batch=batch,
        )
        images = await client.generate_image(workflow=workflow)
        app_logger.debug("Image generated")
        # currently return only one due to business reason
        return images
