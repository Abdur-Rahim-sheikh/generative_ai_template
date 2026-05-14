import pytest

from ....services import BillingService, ImageService
from ....utils.image import decode_base64_to_image
from ...dummies import DummyImageGenerator
from ....domain.exceptions import InsufficientFunds


class TestImageGenerationService:
    @pytest.fixture
    def image_generator(self) -> DummyImageGenerator:
        return DummyImageGenerator()

    @pytest.fixture
    def image_service(self, fake_billing_service: BillingService) -> ImageService:
        return ImageService(
            image_generator=self.image_generator, billing=fake_billing_service
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
        with pytest.raises(InsufficientFunds):
            await image_service.generate_product_image(
                "WRONG_ID", "TEMP", "TEMP", "TEMP", 1, 1
            )
