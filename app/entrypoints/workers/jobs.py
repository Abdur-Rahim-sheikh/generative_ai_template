from uuid import UUID

from ...config import app_logger
from ...dependencies.ai_services import get_image_service


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
    image_service = get_image_service()
    return await image_service.generate_realistic_image(
        wallet_id=wallet_id,
        product_id=product_id,
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
    image_service = get_image_service()
    return await image_service.generate_product_image(
        wallet_id=wallet_id,
        product_id=product_id,
        reference_image=reference_image,
        prompt=prompt,
        width=width,
        height=height,
        batch=batch,
    )
