from ..interfaces import BaseUnitOfWork
from uuid import UUID
from ..domain.exceptions import NotFound, InsufficientFunds
from ..domain.models import Transaction


class BillingService:
    def __init__(self, uow: BaseUnitOfWork):
        self.uow = uow

    async def transact(self, wallet_id: UUID, product_title: str):

        async with self.uow as uow:
            wallet = await uow.wallets.get(wallet_id)

            if not wallet:
                raise NotFound(f"Wallet not found with {wallet_id=}")

            product = await uow.products.get_by_title(product_title)
            if not product:
                raise NotFound(f"Product not found with {product_title=}")

            if wallet.free_uses_remaining >= product.coin_cost:
                wallet.free_uses_remaining -= product.coin_cost
            elif wallet.coin_balance >= product.coin_cost:
                wallet.coin_balance -= product.coin_cost
            else:
                raise InsufficientFunds("Insufficient coin to process")

            await uow.wallets.save(wallet)
            tx = Transaction(
                wallet_id=wallet_id,
                product_id=product_title,
                amount=product.coin_cost,
                type="credit",
            )
            await uow.transactions.save(data=tx)
            await uow.flush()

    async def check_balance(self, wallet_id: UUID):
        pass
