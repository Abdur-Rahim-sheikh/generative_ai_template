from pydantic import BaseModel, computed_field, field_validator, Field

from ..utils.image import decode_base64_to_image


class PromptToImage(BaseModel):
    prompt: str
    ratio: str

    @field_validator("ratio", mode="before")
    @classmethod
    def ratio_filter(cls, value: str) -> str:
        accepted_ratios = ("1:1", "2:3", "3:2")
        if value in accepted_ratios:
            return value
        raise ValueError(f"only accepted ratios are {accepted_ratios}")


class PromptAndImageToImage(PromptToImage):
    base64_image: str

    @field_validator("base64_image", mode="before")
    @classmethod
    def base64_image_validator(cls, value: str) -> str:
        try:
            img = decode_base64_to_image(value)
            img.verify()
            return value
        except Exception as e:
            raise ValueError("The image must be a valid base64 image") from e


class PromptAndImageToImageRequest(PromptAndImageToImage):
    batch: int = Field(default=1, ge=1, le=4)

    @computed_field
    @property
    def width(self) -> int:
        x = int(self.ratio.split(":")[0])
        if x == 1:
            return 1024
        multiplier = 512
        return x * multiplier

    @computed_field
    @property
    def height(self) -> int:
        x = int(self.ratio.split(":")[-1])
        if x == 1:
            return 1024
        multiplier = 512
        return x * multiplier


class PromptToImageRequest(PromptToImage):
    batch: int = Field(default=1, ge=1, le=4)

    @computed_field
    @property
    def width(self) -> int:
        x = int(self.ratio.split(":")[0])
        if x == 1:
            return 1024
        multiplier = 512
        return x * multiplier

    @computed_field
    @property
    def height(self) -> int:
        x = int(self.ratio.split(":")[-1])
        if x == 1:
            return 1024
        multiplier = 512
        return x * multiplier
