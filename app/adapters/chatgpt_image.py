from ..interfaces import BaseImageGenerator


class ChatGPTImage(BaseImageGenerator):
    """Now we can implement this which shares the same interface as the comfyui does,
    Finally, a way to put both under the same umbrella.
    """

    async def generate(self, prompt, width, height, batch=1):
        raise NotImplementedError

    async def edit(self, prompt, reference_image, width, height, batch=1):
        raise NotImplementedError
