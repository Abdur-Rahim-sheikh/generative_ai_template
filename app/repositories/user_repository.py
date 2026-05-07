from uuid import UUID

from sqlmodel import select

from ..domain import User
from ..interfaces.base_repository import BaseUserRepository


class UserRepository(BaseUserRepository):
    async def save(self, data: User) -> User:
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def get(self, id: UUID) -> User:
        result = await self.session.exec(select(User).where(User.id == id))
        return result.scalars().first()

    async def delete(self, id: UUID) -> None:
        user = await self.get(id)
        if user:
            await self.session.delete(user)
            await self.session.commit()

    async def get_by_email(self, email: str) -> User:
        result = await self.session.exec(select(User).where(User.email == email))
        return result.scalars().first()
