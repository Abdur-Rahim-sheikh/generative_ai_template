from datetime import datetime, timedelta, timezone
from uuid import UUID

from ..domain.models import UserSession
from ..interfaces import BaseUnitOfWork


class UserSessionService:
    def __init__(self, uow: BaseUnitOfWork):
        self.uow = uow

    async def create_user_session(
        self, user_id: UUID, expire: timedelta = timedelta(minutes=30)
    ) -> UserSession:
        async with self.uow as uow:
            expires_at = datetime.now(timezone.utc) + expire
            new_session = UserSession(user_id=user_id, expires_at=expires_at)
            await uow.user_sessions.save(new_session)
            return new_session

    async def get_user_session(self, session_id: UUID) -> UserSession | None:
        async with self.uow as uow:
            session = await uow.user_sessions.get(session_id)

            if session and session.expires_at > datetime.now(timezone.utc):
                return session
            return None

    async def regenerate_user_session(
        self, old_session_id: UUID, expire: timedelta = timedelta(minutes=30)
    ) -> UserSession | None:
        session = await self.get_user_session(old_session_id)
        if not session:
            return None

        new_session = await self.create_user_session(session.user_id, expire)
        await self.delete_user_session(session.id)
        return new_session

    async def delete_user_session(self, session_id: UUID) -> None:
        async with self.uow as uow:
            await uow.user_sessions.delete(session_id)
