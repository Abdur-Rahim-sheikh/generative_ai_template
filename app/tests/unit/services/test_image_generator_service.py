from unittest.mock import AsyncMock

import pytest

from ....domain.exceptions import InsufficientFunds, NotFound
from ....domain.models import Product, Wallet
from ....services import BillingService, ImageService
from ....utils.image import decode_base64_to_image
from ...dummies import DummyImageGenerator


class TestImageGenerationService:
    @pytest.fixture
    def image_generator(self) -> DummyImageGenerator:
        return DummyImageGenerator()

    @pytest.fixture
    def image_service(
        self, image_generator: DummyImageGenerator, fake_billing_service: BillingService
    ) -> ImageService:
        return ImageService(
            image_generator=image_generator, billing=fake_billing_service
        )

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

    async def test_missing_wallet_id(self, image_service: ImageService):
        with pytest.raises(
            NotFound, match="Wallet not found with wallet_id='WRONG_ID'"
        ):
            await image_service.generate_product_image(
                "WRONG_ID", "TEMP", "TEMP", "TEMP", 1, 1
            )

    async def test_missing_product_id(self, image_service: ImageService):
        wallet = Wallet(user_id="USERID", coin_balance=50, free_uses_remaining=5)
        await image_service.billing.uow.wallets.save(data=wallet)
        with pytest.raises(
            NotFound, match="Product not found with product_id='WRONG_ID'"
        ):
            await image_service.generate_product_image(
                wallet.id, "WRONG_ID", "TEMP", "TEMP", 1, 1
            )

    async def test_happy_image_generation(self, image_service: ImageService):

        COIN_BALANCE = 50
        FREE_USES_REMAINING = 5
        wallet = Wallet(
            user_id="USERID",
            coin_balance=COIN_BALANCE,
            free_uses_remaining=FREE_USES_REMAINING,
        )
        await image_service.billing.uow.wallets.save(data=wallet)

        COIN_COST = 20
        product = Product(title="LLM-custom", coin_cost=COIN_COST, unit="second")
        await image_service.billing.uow.products.save(data=product)

        images = await image_service.generate_realistic_image(
            wallet_id=wallet.id, product_id=product.id, prompt="TEMP", width=1, height=1
        )

        assert len(images) == 1
        current_wallet = await image_service.billing.uow.wallets.get(wallet.id)

        assert current_wallet.coin_balance == COIN_BALANCE - COIN_COST
        assert current_wallet.free_uses_remaining == FREE_USES_REMAINING

    async def test_happy_image_generation_with_free_coin(
        self, image_service: ImageService
    ):

        COIN_BALANCE = 50
        FREE_USES_REMAINING = 5
        wallet = Wallet(
            user_id="USERID",
            coin_balance=COIN_BALANCE,
            free_uses_remaining=FREE_USES_REMAINING,
        )
        await image_service.billing.uow.wallets.save(data=wallet)

        COIN_COST = 5
        product = Product(title="LLM-custom", coin_cost=COIN_COST, unit="second")
        await image_service.billing.uow.products.save(data=product)

        images = await image_service.generate_realistic_image(
            wallet_id=wallet.id, product_id=product.id, prompt="TEMP", width=1, height=1
        )

        assert len(images) == 1
        current_wallet = await image_service.billing.uow.wallets.get(wallet.id)

        assert current_wallet.coin_balance == COIN_BALANCE
        assert current_wallet.free_uses_remaining == FREE_USES_REMAINING - COIN_COST

    async def test_insufficient_balance_exception(self, image_service: ImageService):
        COIN_BALANCE = 50
        FREE_USES_REMAINING = 5
        wallet = Wallet(
            user_id="USERID",
            coin_balance=COIN_BALANCE,
            free_uses_remaining=FREE_USES_REMAINING,
        )
        await image_service.billing.uow.wallets.save(data=wallet)

        COIN_COST = 60
        product = Product(title="LLM-custom", coin_cost=COIN_COST, unit="second")
        await image_service.billing.uow.products.save(data=product)
        with pytest.raises(InsufficientFunds):
            await image_service.generate_realistic_image(
                wallet_id=wallet.id,
                product_id=product.id,
                prompt="TEMP",
                width=1,
                height=1,
            )
        assert wallet.coin_balance == COIN_BALANCE
        assert wallet.free_uses_remaining == FREE_USES_REMAINING

    async def test_generator_failure_does_not_revert_billing(
        self, image_service: ImageService
    ):
        COIN_BALANCE = 50
        FREE_USES_REMAINING = 5
        wallet = Wallet(
            user_id="USERID",
            coin_balance=COIN_BALANCE,
            free_uses_remaining=FREE_USES_REMAINING,
        )
        await image_service.billing.uow.wallets.save(data=wallet)

        COIN_COST = 30
        product = Product(title="LLM-custom", coin_cost=COIN_COST, unit="second")
        await image_service.billing.uow.products.save(data=product)

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
