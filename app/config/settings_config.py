from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    DEBUG: bool = True

    # llm config
    OLLAMA_MODEL: str = "phi4-mini:3.8b"
    OLLAMA_HOST: str
    OPENAI_LLM_MODEL: str
    OPENAI_IMAGE_MODEL: str
    OPENAI_API_KEY: str

    # tts config
    COQUI_HOST: str = "tts"
    COQUI_PORT: str = "8020"
    ELEVENLAB_API: str

    # db config
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: SecretStr

    # Comfy connection
    COMFY_HOST: str
    COMFY_PORT: int

    class Config:
        env_file = ".env"


settings = Settings()
