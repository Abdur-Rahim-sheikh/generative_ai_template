from uuid import uuid4

import pytest

from ....domain.models import Wallet
from ...fakes import FakeWalletRepository
from .base import BaseRepositoryCommonTests


class TestWalletRepository(BaseRepositoryCommonTests):
    @pytest.fixture
    def repo(self) -> FakeWalletRepository:
        return FakeWalletRepository()

    @pytest.fixture
    def sample_entity(self) -> Wallet:
        return Wallet(coin_balance=2, free_uses_remaining=4)

    async def test_get_by_user_id(self, repo: FakeWalletRepository):
        user_id = uuid4()
        wallet = Wallet(
            user_id=user_id,
        )
        await repo.save(wallet)
        wallet2 = await repo.get_by_user_id(user_id=user_id)
        assert wallet2 == wallet
