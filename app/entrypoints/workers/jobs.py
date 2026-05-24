from uuid import UUID

from ...config import app_logger
from ...dependencies.ai_services import image_service_worker_ctx


async def realistic_image(
    ctx,
    wallet_id: UUID,
    product_id: UUID,
    prompt: str,
    width: int,
    height: int,
    batch: int = 1,
) -> list[str]:
    app_logger.debug(msg=f"enhanced: {prompt=}")
    async with image_service_worker_ctx() as image_service:
        return await image_service.generate_realistic_image(
            wallet_id=wallet_id,
            product_title=product_id,
            prompt=prompt,
            width=width,
            height=height,
            batch=batch,
        )


async def product_photography(
    ctx,
    wallet_id: UUID,
    product_id: UUID,
    reference_image: bytes,
    prompt: str,
    width: int,
    height: int,
    batch: int = 1,
) -> list[str]:
    async with image_service_worker_ctx() as image_service:
        return await image_service.generate_product_image(
            wallet_id=wallet_id,
            product_title=product_id,
            reference_image=reference_image,
            prompt=prompt,
            width=width,
            height=height,
            batch=batch,
        )
