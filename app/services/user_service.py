from uuid import UUID

from ..domain import User, Wallet
from ..interfaces import BaseUnitOfWork
from ..schemas.user import CreateUserRequest


class UserService:
    def __init__(self, uow: BaseUnitOfWork):
        self.uow = uow

    async def create_user(self, data: CreateUserRequest) -> User:
        async with self.uow as uow:
            new_user = User(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                hashed_password=data.hashed_password,
            )
            await uow.users.save(new_user)

            new_wallet = Wallet(user=new_user, free_uses_remaining=50)

            await uow.wallets.save(new_wallet)
            return new_user

    async def get_user(self, user_id: UUID) -> User:
        async with self.uow as uow:
            user = await uow.users.get(user_id)
            return user

    async def delete_user(self, user_id: UUID) -> None:
        async with self.uow as uow:
            await uow.users.delete(user_id)

    async def get_user_by_email(self, email: str) -> User:
        async with self.uow as uow:
            user = await uow.users.get_by_email(email)
            return user
