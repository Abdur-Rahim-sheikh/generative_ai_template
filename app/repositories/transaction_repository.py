from ..interfaces.base_repository import BaseTransactionRepository
from ..domain import Transaction
from uuid import UUID
from sqlmodel import select


class TransactionRepository(BaseTransactionRepository):
    async def save(self, data: Transaction) -> Transaction:
        self.session.add(data)
        return data

    async def get(self, id: UUID) -> Transaction | None:
        transaction = await self.session.get(UUID, id)
        return transaction

    async def delete(self, id: UUID) -> None:
        transaction = await self.get(id)
        if transaction:
            await self.session.delete(transaction)

    async def get_by_wallet_id(self, wallet_id: UUID) -> Transaction:
        return self.session.execute(
            select(Transaction).where(Transaction.wallet_id == wallet_id)
        )
