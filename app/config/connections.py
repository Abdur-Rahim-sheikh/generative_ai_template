from typing import AsyncGenerator

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .settings_config import settings

if settings.DB_HOST:
    db_url = URL.create(
        "postgresql+asyncpg",
        username=settings.DB_USER,
        password=settings.DB_PASSWORD.get_secret_value(),
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    )
else:
    db_url = "sqlite+aiosqlite:///resources/db.sqlite3"

async_engine = create_async_engine(db_url, echo=True, future=True)


async_session_maker = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# async def init_db():
#     from ..domain.models import User, Product, Wallet, Transaction, UserSession  # noqa: F401

#     async with async_engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)


# async def drop_db():
#     from ..domain.models import User, Product, Wallet, Transaction, UserSession  # noqa: F401

#     async with async_engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.drop_all)
