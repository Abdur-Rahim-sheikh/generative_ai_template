from uuid import UUID

from ..domain import User
from ..repositories import UnitOfWork
from ..schemas.user import CreateUserRequest


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_user(self, data: CreateUserRequest) -> User:
        async with self.uow as uow:
            user_data = User(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                hashed_password=data.hashed_password,
            )
            saved = await uow.users.save(user_data)
            return saved

    async def get_user(self, user_id: UUID) -> User:
        pass

    async def delete_user(self, user_id: UUID) -> None:
        pass

    async def get_user_by_email(self, email: str) -> User:
        pass
