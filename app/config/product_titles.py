from dataclasses import dataclass


@dataclass(frozen=True)
class ProductTitle:
    GENERATED_SCRIPT: str = "generated-script"
    GENERATED_TTS: str = "generated-tts"
    REALISTIC_IMAGE: str = "realistic-image"
    PRODUCT_IMAGE: str = "product-image"
