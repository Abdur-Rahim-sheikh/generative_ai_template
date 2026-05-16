import pytest
from ...fakes import FakeUnitOfWork
from ....domain.models import Wallet, Product


@pytest.fixture(autouse=True)
async def seeded_db(fake_uow: FakeUnitOfWork):
    wallet = Wallet(id="test-wallet-id", user_id="test-user", coin_balance=20)
    product = Product(id="test-product-id", title="test-title", coin_cost=10)
    await fake_uow.wallets.save(wallet)
    await fake_uow.products.save(product)
