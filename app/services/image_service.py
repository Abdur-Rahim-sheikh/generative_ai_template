from ..interfaces import BaseImageGenerator
from uuid import UUID
from .billing_service import BillingService


class ImageService:
    def __init__(self, image_generator: BaseImageGenerator, billing: BillingService):
        self.image_generator = image_generator
        self.billing = billing

    async def generate_realistic_image(
        self,
        wallet_id: UUID,
        product_id: UUID,
        prompt: str,
        width: int,
        height: int,
        batch: int = 1,
    ) -> list[str]:
        await self.billing.transact(wallet_id=wallet_id, product_id=product_id)

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
        await self.billing.transact(wallet_id=wallet_id, product_id=product_id)

        return await self.image_generator.edit(
            prompt=prompt,
            reference_image=reference_image,
            width=width,
            height=height,
            batch=batch,
        )
