from redis.asyncio import ConnectionError, Redis

from ..config import app_logger, settings
from ..interfaces import NoSQL
from ..utils import singleton


@singleton
class RedisClient(NoSQL):
    def __init__(
        self,
        host: str = settings.REDIS_HOST,
        port: int = settings.REDIS_PORT,
        password: str = settings.REDIS_PASSWORD.get_secret_value(),
        db: int = settings.REDIS_DB,
    ):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.client: Redis | None = None

    async def connect(self) -> bool:
        if self.client:
            return

        try:
            self.client = Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                db=self.db,
                decode_responses=True,
                socket_keepalive=True,
            )

            return await self.client.ping()
        except ConnectionError as e:
            app_logger.error(f"Redis connection error {e}")
            raise RuntimeError("Redis connection error") from e

    async def disconnect(self):
        if self.client:
            await self.client.close()
        self.client = None

    async def set_data(
        self, key: str, value: str | bytes | bytearray, exp: int = 604800
    ):
        try:
            return await self.client.set(name=key, value=value, ex=exp)
        except Exception as e:
            app_logger.exception(f"redis set failed {e}")
            raise RuntimeError("error setting key to value") from e

    async def get_data(self, key: str):
        return await self.client.get(key)
