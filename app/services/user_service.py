from uuid import UUID

from ..domain.models import User, Wallet
from ..domain.exceptions import NotFound
from ..interfaces import BaseUnitOfWork
from ..schemas.user import CreateUserRequest


class UserService:
    def __init__(self, uow: BaseUnitOfWork):
        self.uow = uow

    async def create_user(
        self, data: CreateUserRequest, initial_free_uses: int = 50
    ) -> User:
        async with self.uow as uow:
            new_user = User(
                id=None,
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                hashed_password=data.hashed_password,
            )
            await uow.users.save(new_user)

            new_wallet = Wallet(user=new_user, free_uses_remaining=initial_free_uses)

            await uow.wallets.save(new_wallet)
            return new_user

    async def get_user(self, user_id: UUID) -> User | None:
        async with self.uow as uow:
            user = await uow.users.get(user_id)
            if not user:
                raise NotFound(f"User Not Found by this {user_id=}")
            return user

    async def delete_user(self, user_id: UUID) -> None:
        async with self.uow as uow:
            await uow.users.delete(user_id)

    async def get_user_by_email(self, email: str) -> User:
        async with self.uow as uow:
            user = await uow.users.get_by_email(email)
            if not user:
                raise NotFound(f"User not found to this {email=}")
            return user
