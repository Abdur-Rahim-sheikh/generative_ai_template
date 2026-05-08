from sqlalchemy.ext.asyncio import AsyncSession

from ..interfaces import BaseUnitOfWork
from .user_repository import UserRepository


class UnitOfWork(BaseUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session
        self.users = UserRepository(self._session)

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

        await self._session.close()
