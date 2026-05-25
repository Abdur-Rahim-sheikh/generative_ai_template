import dataclasses


@dataclasses.dataclass(frozen=True)
class ProductTitle:
    GENERATED_SCRIPT: str = "generated-script"
    GENERATED_TTS: str = "generated-tts"
    REALISTIC_IMAGE: str = "realistic-image"
    PRODUCT_IMAGE: str = "product-image"

    def __iter__(self):
        yield from dataclasses.asdict(self).values()
