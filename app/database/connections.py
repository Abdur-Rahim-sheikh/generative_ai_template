from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from ..config import settings

# db_url = settings.DB_HOST  or "sqlite+aiosqlite:///./db.sqlite3"
db_url = (
    f"postgresql+asyncpg://{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_USER}"
    if settings.DB_HOST
    else "sqlite+aiosqlite:///./db.sqlite3"
)
async_engine = create_async_engine(db_url, echo=True, future=True)


async_session_maker = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def init_db():
    from .models import User, Product, Wallet, Transaction, Session  # noqa: F401

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_db():
    from .models import User, Product, Wallet, Transaction, Session  # noqa: F401

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
