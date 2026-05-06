from arq.connections import RedisSettings
from .jobs import realistic_image, product_photography
from ...config import settings

REDIS_SETTINGS = RedisSettings(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    database=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD.get_secret_value(),
)


class WorkerSettings:
    functions = [realistic_image, product_photography]
    redis_settings = REDIS_SETTINGS
    max_jobs = 6
    job_timeout = 900
    keep_result_during = 1800
    max_retries = 3
