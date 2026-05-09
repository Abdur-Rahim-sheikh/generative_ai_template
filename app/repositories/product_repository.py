from uuid import UUID

from sqlmodel import select

from ..domain import Product
from ..interfaces.base_repository import BaseProductRepository


class ProductRepository(BaseProductRepository):
    async def save(self, data: Product) -> Product:
        self.session.add(data)
        return data

    async def get(self, id: UUID) -> Product:
        result = await self.session.exec(select(Product).where(Product.id == id))
        return result.first()

    async def delete(self, id: UUID) -> None:
        product = await self.get(id)
        if product:
            await self.session.delete(product)
