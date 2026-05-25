from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi.security import OAuth2PasswordBearer


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

    # jwt config
    JWT_SECRET_KEY: SecretStr = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
