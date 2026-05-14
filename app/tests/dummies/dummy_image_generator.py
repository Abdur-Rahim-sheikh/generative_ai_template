from random import randint

from PIL import Image
from ...utils.image import encode_image_to_base64
from ...interfaces import BaseImageGenerator


class DummyImageGenerator(BaseImageGenerator):
    """
    Dummy Image Generator
    """

    def _get_images(self, width: int, height: int, batch):
        images = []
        for _ in range(batch):
            r, g = 127, 127
            b = randint(1, 255)
            image = Image.new("RGB", (width, height), (r, g, b))
            images.append(encode_image_to_base64(image))
        return images

    async def generate(self, prompt, width, height, batch=1) -> list[str]:
        return self._get_images(width, height, batch)

    async def edit(self, prompt, reference_image, width, height, batch=1) -> list[str]:
        return self._get_images(width, height, batch)
