from ..interfaces import BaseUnitOfWork
from uuid import UUID
from ..domain.exceptions import NotFound, InsufficientFunds
from ..domain.models import Transaction


class BillingService:
    def __init__(self, uow: BaseUnitOfWork):
        self.uow = uow

    async def transact(self, wallet_id: UUID, product_id: UUID):

        async with self.uow as uow:
            product = await uow.products.get(product_id)
            wallet = await uow.wallets.get(wallet_id)
            if not product:
                raise NotFound(f"Product not found with {product_id=}")
            if not wallet:
                raise NotFound(f"Wallet not found with {wallet_id=}")

            if wallet.free_uses_remaining >= product.coin_cost:
                wallet.free_uses_remaining -= product.coin_cost
            elif wallet.coint_balance >= product.coin_cost:
                wallet.coin_balance -= product.coin_cost
            else:
                raise InsufficientFunds("Insufficient coin to process")

            await uow.wallets.save(wallet)
            tx = Transaction(
                wallet_id=wallet_id,
                product_id=product_id,
                amount=product.coin_cost,
                type="credit",
            )
            await uow.transactions.save(data=tx)
            await uow.flush()

    async def check_balance(self, wallet_id: UUID):
        pass
