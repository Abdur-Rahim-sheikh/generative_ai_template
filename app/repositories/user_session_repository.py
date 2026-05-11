from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import delete as delete_statement
from sqlmodel import select

from ..domain import UserSession
from ..domain.exceptions import AlreadyExists
from ..interfaces.base_repository import BaseUserSessionRepository


class UserSessionRepository(BaseUserSessionRepository):
    async def save(self, data: UserSession) -> UserSession:
        try:
            self.session.add(data)
            self.session.flush()
        except IntegrityError:
            raise AlreadyExists("This session already exists")

    async def get(self, id: UUID) -> UserSession | None:
        return await self.session.get(UserSession, id)

    async def delete(self, id: UUID):
        statement = delete_statement(UserSession).where(UserSession.id == id)
        await self.session.execute(statement=statement)
        await self.session.flush()

    async def get_by_user_id(self, user_id: UUID) -> UserSession | None:
        return await self.session.execute(
            select(UserSession).where(UserSession.user_id == user_id)
        )
