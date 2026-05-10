from uuid import UUID

from sqlmodel import select

from ..domain import UserSession
from ..interfaces.base_repository import BaseUserSessionRepository


class UserSessionRepository(BaseUserSessionRepository):
    async def save(self, data: UserSession) -> UserSession:
        self.session.add(data)

    async def get(self, id: UUID) -> UserSession | None:
        return await self.session.get(UserSession, id)

    async def delete(self, id: UUID):
        session = await self.get(id)
        if session:
            await self.session.delete(session)

    async def get_by_user_id(self, user_id: UUID) -> UserSession | None:
        return await self.session.execute(
            select(UserSession).where(UserSession.user_id == user_id)
        )
