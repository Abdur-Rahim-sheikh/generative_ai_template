from uuid import UUID

from sqlmodel import select, delete as table_delete

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
        statement = table_delete(User).where(User.id == id)
        await self.session.execute(statement=statement)
        await self.session.flush()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.first()
