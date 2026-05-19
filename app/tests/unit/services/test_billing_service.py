import pytest

from ....domain.exceptions import NotFound, InsufficientFunds
from ....domain.models import Wallet
from ....services import BillingService
from .conftest import SeedDbFactory


async def test_missing_wallet_id(billing_service: BillingService):
    with pytest.raises(NotFound, match="Wallet not found with wallet_id='WRONG_ID'"):
        await billing_service.transact("WRONG_ID", "TEMP")


async def test_missing_product_id(billing_service: BillingService):
    wallet = Wallet(user_id="USERID", coin_balance=50, free_uses_remaining=5)
    await billing_service.uow.wallets.save(data=wallet)
    with pytest.raises(NotFound, match="Product not found with product_id='WRONG_ID'"):
        await billing_service.transact(wallet.id, "WRONG_ID")


async def test_insufficient_balance_exception(
    billing_service: BillingService, seeded_db: SeedDbFactory
):
    COIN_BALANCE = 50
    FREE_USES_REMAINING = 5
    COIN_COST = 60

    wallet, product = await seeded_db(
        coin_balance=COIN_BALANCE,
        free_uses_remaining=FREE_USES_REMAINING,
        coin_cost=COIN_COST,
    )

    with pytest.raises(InsufficientFunds):
        await billing_service.transact(
            wallet_id=wallet.id,
            product_id=product.id,
        )

    assert wallet.coin_balance == COIN_BALANCE
    assert wallet.free_uses_remaining == FREE_USES_REMAINING


async def test_happy_path(billing_service: BillingService, seeded_db: SeedDbFactory):
    COIN_BALANCE = 50
    FREE_USES_REMAINING = 5
    COIN_COST = 10
    wallet, product = await seeded_db(
        coin_balance=COIN_BALANCE,
        free_uses_remaining=FREE_USES_REMAINING,
        coin_cost=COIN_COST,
    )

    await billing_service.transact(
        wallet_id=wallet.id,
        product_id=product.id,
    )
