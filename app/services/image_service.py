from ..interfaces import BaseImageGenerator
from uuid import UUID


class ImageService:
    def __init__(self, image_generator: BaseImageGenerator):
        self.image_generator = image_generator

    async def generate_realistic_image(
        self,
        wallet_id: UUID,
        product_id: UUID,
        prompt: str,
        width: int,
        height: int,
        batch: int = 1,
    ) -> list[str]:
        return await self.image_generator.generate(
            prompt=prompt, width=width, height=height, batch=batch
        )

    async def generate_product_image(
        self,
        wallet_id: UUID,
        product_id: UUID,
        prompt: str,
        reference_image: bytes,
        width: int,
        height: int,
        batch: int = 1,
    ) -> list[str]:
        return await self.image_generator.edit(
            prompt=prompt,
            reference_image=reference_image,
            width=width,
            height=height,
            batch=batch,
        )
