from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlmodel import delete as table_delete
from sqlmodel import select


from ..domain.exceptions import AlreadyExists
from ..domain.models import User
from ..interfaces.base_repository import BaseUserRepository


class UserRepository(BaseUserRepository):
    async def save(self, data: User):
        try:
            self.session.add(data)
            await self.session.flush()

            return data
        except IntegrityError:
            raise AlreadyExists("User Already exists")

    async def get(self, id: UUID) -> User | None:
        result = await self.session.execute(
            select(User).options(joinedload(User.wallet)).where(User.id == id)
        )

        return result.scalar_one_or_none()

    async def delete(self, id: UUID) -> None:
        statement = table_delete(User).where(User.id == id)
        await self.session.execute(statement=statement)
        await self.session.flush()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).options(joinedload(User.wallet)).where(User.email == email)
        )
        return result.scalar_one_or_none()
