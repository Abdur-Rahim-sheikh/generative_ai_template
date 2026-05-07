from ..interfaces.base_repository import BaseUserRepository
from ..domain import User
from uuid import UUID


class UserService:
    def __init__(self, user_repository: BaseUserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_data: User) -> User:
        user = await self.user_repository.save(user_data)
        return user

    async def get_user(self, user_id: UUID) -> User:
        pass

    async def delete_user(self, user_id: UUID) -> None:
        pass

    async def get_user_by_email(self, email: str) -> User:
        pass
