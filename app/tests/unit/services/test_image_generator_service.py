from unittest.mock import AsyncMock

import pytest

from ....services import BillingService, ImageService
from ....utils.image import decode_base64_to_image
from ...dummies import DummyImageGenerator
from .conftest import SeedDbFactory


class TestImageGenerationService:
    @pytest.fixture
    def image_generator(self) -> DummyImageGenerator:
        return DummyImageGenerator()

    @pytest.fixture
    def image_service(
        self, image_generator: DummyImageGenerator, billing_service: BillingService
    ) -> ImageService:
        return ImageService(image_generator=image_generator, billing=billing_service)

    async def test_returned_image(self, image_generator: DummyImageGenerator):
        m, n = 360, 360
        images = await image_generator.generate("hello", width=m, height=n)

        assert isinstance(images, list)
        images = [decode_base64_to_image(image) for image in images]

        assert len(images) == 1

        assert images[0].size == (m, n)

    async def test_multi_generation(self, image_generator: DummyImageGenerator):
        m, n = 720, 720
        batch = 4
        images = await image_generator.edit(
            "HEllo", "hi", width=m, height=n, batch=batch
        )
        assert len(images) == batch

    async def test_happy_image_generation(
        self, image_service: ImageService, seeded_db: SeedDbFactory
    ):

        COIN_BALANCE = 50
        FREE_USES_REMAINING = 5
        COIN_COST = 20
        wallet, product = await seeded_db(
            coin_balance=COIN_BALANCE,
            free_uses_remaining=FREE_USES_REMAINING,
            coin_cost=COIN_COST,
        )

        images = await image_service.generate_realistic_image(
            wallet_id=wallet.id, product_id=product.id, prompt="TEMP", width=1, height=1
        )

        assert len(images) == 1
        current_wallet = await image_service.billing.uow.wallets.get(wallet.id)

        assert current_wallet.coin_balance == COIN_BALANCE - COIN_COST
        assert current_wallet.free_uses_remaining == FREE_USES_REMAINING

    async def test_happy_image_generation_with_free_coin(
        self, image_service: ImageService, seeded_db: SeedDbFactory
    ):

        COIN_BALANCE = 50
        FREE_USES_REMAINING = 5
        COIN_COST = 5
        wallet, product = await seeded_db(
            coin_balance=COIN_BALANCE,
            free_uses_remaining=FREE_USES_REMAINING,
            coin_cost=COIN_COST,
        )

        images = await image_service.generate_realistic_image(
            wallet_id=wallet.id, product_id=product.id, prompt="TEMP", width=1, height=1
        )

        assert len(images) == 1
        current_wallet = await image_service.billing.uow.wallets.get(wallet.id)

        assert current_wallet.coin_balance == COIN_BALANCE
        assert current_wallet.free_uses_remaining == FREE_USES_REMAINING - COIN_COST

    async def test_generator_failure_does_not_revert_billing(
        self, image_service: ImageService, seeded_db: SeedDbFactory
    ):
        COIN_BALANCE = 50
        FREE_USES_REMAINING = 5
        COIN_COST = 30

        wallet, product = await seeded_db(
            coin_balance=COIN_BALANCE,
            free_uses_remaining=FREE_USES_REMAINING,
            coin_cost=COIN_COST,
        )

        # mocking the generator
        image_service.image_generator.generate = AsyncMock(
            side_effect=Exception("Inappropriate prompt")
        )
        with pytest.raises(Exception, match="Inappropriate prompt"):
            await image_service.generate_realistic_image(
                wallet_id=wallet.id,
                product_id=product.id,
                prompt="TEMP",
                width=1,
                height=1,
            )
        current_wallet = await image_service.billing.uow.wallets.get(wallet.id)
        assert current_wallet.coin_balance == COIN_BALANCE - COIN_COST
        assert current_wallet.free_uses_remaining == FREE_USES_REMAINING
