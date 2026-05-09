from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    DEBUG: bool = True
    USE_DUMMY_SERVICES: bool = True

    # llm config
    OLLAMA_MODEL: str = "phi4-mini:3.8b"
    OLLAMA_HOST: str

    # tts config
    COQUI_HOST: str = "tts"
    COQUI_PORT: str = "8020"

    # db config
    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_USER: str = "postgres"
    DB_NAME: str = "postgres"
    DB_PASSWORD: SecretStr

    # redis config
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
