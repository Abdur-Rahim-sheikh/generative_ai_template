from .comfy_client import ComfyClient
from ..interfaces import BaseImageGenerator
from .workflow_generator import WorkflowGenerator
from uuid import uuid4


class ComfyImage(BaseImageGenerator):
    """
    The particular workflow calling is not business level logic.
    It's comfy or more specifically adapter level logic. That the generate/edit method
    are hooked with these workflows no confusion.
    """

    def __init__(
        self,
        client: ComfyClient,
        workflow_generator: WorkflowGenerator = WorkflowGenerator(),
    ):
        self.client = client
        self.workflow_generator = workflow_generator

    async def generate(
        self, prompt: str, width: int, height: int, batch: int = 1
    ) -> list[str]:
        workflow = self.workflow_generator.get_realistic_image_workflow(
            prompt, width, height, batch
        )
        async with self.client as client:
            b64_images = await client.generate_image(workflow=workflow)
            return b64_images

    async def edit(
        self,
        prompt: str,
        reference_image: bytes,
        width: int,
        height: int,
        batch: int = 1,
    ) -> list[str]:
        image_name = uuid4().hex[:16]
        async with self.client as client:
            uploaded_img_name = await client.upload_image(
                image_bytes=reference_image, file_name=image_name
            )
            workflow = self.workflow_generator.get_product_image_workflow(
                reference_image_name=uploaded_img_name,
                prompt=prompt,
                width=width,
                height=height,
                batch=batch,
            )

            return await client.generate_image(workflow)
