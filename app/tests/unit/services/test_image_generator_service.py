import pytest

from ....utils.image import decode_base64_to_image
from ...dummies import DummyImageGenerator
from ...fakes import FakeUnitOfWork


class TestImageGenerationService:
    @pytest.fixture
    def uow(self) -> FakeUnitOfWork:
        return FakeUnitOfWork()

    @pytest.fixture
    def image_generator(self) -> DummyImageGenerator:
        return DummyImageGenerator()

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
