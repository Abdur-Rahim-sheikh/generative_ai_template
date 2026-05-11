from uuid import UUID

from sqlmodel import select, delete as delete_statement

from ..domain import Product
from ..interfaces.base_repository import BaseProductRepository
from ..domain.exceptions import AlreadyExists
from sqlalchemy.exc import IntegrityError


class ProductRepository(BaseProductRepository):
    async def save(self, data: Product):
        try:
            self.session.add(data)
            self.session.flush()
        except IntegrityError:
            raise AlreadyExists("The Product already exists with this title")

    async def get(self, id: UUID) -> Product:
        result = await self.session.exec(select(Product).where(Product.id == id))
        return result.first()

    async def delete(self, id: UUID) -> None:
        statement = delete_statement(Product).where(Product.id == id)
        await self.session.execute(statement)
        await self.session.flush()
