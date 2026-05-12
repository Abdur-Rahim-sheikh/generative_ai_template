from uuid import UUID

from sqlmodel import select

from ..domain import Transaction
from ..interfaces.base_repository import BaseTransactionRepository


class TransactionRepository(BaseTransactionRepository):
    async def save(self, data: Transaction):
        self.session.add(data)
        self.session.flush()

    async def get(self, id: UUID) -> Transaction | None:
        transaction = await self.session.get(UUID, id)
        return transaction

    async def delete(self, id: UUID) -> None:
        raise NotImplementedError("Transaction should not be directly deleted")

    async def get_by_wallet_id(self, wallet_id: UUID) -> Transaction:
        wallet = await self.session.execute(
            select(Transaction).where(Transaction.wallet_id == wallet_id)
        )
        return wallet.scalar_one_or_none()
