from ..interfaces.base_repository import BaseWalletRepository
from ..domain import Wallet
from uuid import UUID
from sqlmodel import select


class WalletRepository(BaseWalletRepository):
    async def save(self, data: Wallet) -> Wallet:
        self.session.add(data)

    async def get(self, id: UUID) -> Wallet:
        wallet = await self.session.get(Wallet, id)
        return wallet

    async def delete(self, id: UUID):
        wallet = await self.get(id)
        if wallet:
            await self.session.delete(wallet)

    async def get_by_user_id(self, user_id: UUID) -> Wallet:
        wallet = await self.session.exec(
            select(Wallet).where(Wallet.user_id == user_id)
        )

        return wallet
