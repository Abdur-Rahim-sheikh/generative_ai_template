import pytest
from ...fakes import FakeUnitOfWork
from ....domain.models import Wallet, Product

from typing import Protocol, Awaitable


class SeedDbFactory(Protocol):
    def __call__(
        self, coin_balance: int = 20, free_uses_remaining: int = 5, coin_cost: int = 10
    ) -> Awaitable[tuple[Wallet, Product]]: ...


@pytest.fixture
async def seeded_db(fake_uow: FakeUnitOfWork) -> SeedDbFactory:
    async def _seed_db(
        coin_balance: int = 20, free_uses_remaining: int = 5, coin_cost: int = 10
    ) -> tuple[Wallet, Product]:
        wallet = Wallet(
            id="test-wallet-id",
            user_id="test-user",
            coin_balance=coin_balance,
            free_uses_remaining=free_uses_remaining,
        )
        product = Product(
            id="test-product-id", title="test-title", coin_cost=coin_cost, unit="second"
        )
        await fake_uow.wallets.save(wallet)
        await fake_uow.products.save(product)

        return wallet, product

    return _seed_db
