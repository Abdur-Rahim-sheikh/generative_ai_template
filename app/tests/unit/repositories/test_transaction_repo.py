from uuid import uuid4

import pytest

from ....domain.models import Transaction
from ...fakes import FakeTransactionRepository
from .base import BaseRepositoryCommonTests


class TestTransactionRepository(BaseRepositoryCommonTests):
    @pytest.fixture
    def repo(self) -> FakeTransactionRepository:
        return FakeTransactionRepository()

    @pytest.fixture
    def sample_entity(self) -> Transaction:
        return Transaction(type="credit", amount=5)

    async def test_get_by_wallet_id(self, repo: FakeTransactionRepository):
        wallet_id = uuid4()
        transaction = Transaction(type="credit", amount=5, wallet_id=wallet_id)
        transaction2 = Transaction(type="debit", amount=56, wallet_id=wallet_id)
        await repo.save(transaction)
        await repo.save(transaction2)
        returend_transactions = await repo.get_by_wallet_id(wallet_id=wallet_id)

        assert len(returend_transactions) == 2
