from uuid import UUID

from sqlmodel import select

from ..domain import User
from ..interfaces.base_repository import BaseUserRepository
from sqlalchemy.exc import IntegrityError
from ..domain.exceptions import AlreadyExists


class UserRepository(BaseUserRepository):
    async def save(self, data: User):
        try:
            self.session.add(data)
            await self.session.flush()

            return data
        except IntegrityError:
            raise AlreadyExists("User Already exists")

    async def get(self, id: UUID) -> User:
        result = await self.session.exec(select(User).where(User.id == id))
        return result.first()

    async def delete(self, id: UUID) -> None:
        user = await self.get(id)
        if user:
            await self.session.delete(user)

    async def get_by_email(self, email: str) -> User:
        result = await self.session.exec(select(User).where(User.email == email))
        return result.first()
