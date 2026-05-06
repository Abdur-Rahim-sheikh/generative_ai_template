from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..config import settings

db_url = settings.DB_URL or "sqlite+aiosqlite:///./db.sqlite3"

async_engine = create_async_engine(db_url, echo=True, future=True)


async_session_maker = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=True
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
