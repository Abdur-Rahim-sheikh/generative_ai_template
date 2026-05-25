from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import delete as delete_statement
from sqlmodel import select

from ..domain.models import Wallet
from ..domain.exceptions import AlreadyExists
from ..interfaces.base_repository import BaseWalletRepository


class WalletRepository(BaseWalletRepository):
    async def save(self, data: Wallet) -> Wallet:
        try:
            self.session.add(data)
            await self.session.flush()
        except IntegrityError:
            raise AlreadyExists("This wallet already exists")

    async def get(self, id: UUID) -> Wallet:
        wallet = await self.session.get(Wallet, id)
        return wallet

    async def delete(self, id: UUID):
        statement = delete_statement(Wallet).where(Wallet.id == id)
        await self.session.execute(statement)
        await self.session.flush()

    async def get_by_user_id(self, user_id: UUID) -> Wallet:
        wallet = await self.session.execute(
            select(Wallet).where(Wallet.user_id == user_id)
        )

        return wallet.scalar_one_or_none()
