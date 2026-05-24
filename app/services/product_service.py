from uuid import UUID
from ..interfaces.base_uow import BaseUnitOfWork
from ..domain.models import Product
from ..domain.exceptions import NotFound
from ..schemas.product import CreateProductRequest


class ProductService:
    def __init__(self, uow: BaseUnitOfWork):
        self.uow = uow

    async def create_product(self, data: CreateProductRequest) -> Product:
        async with self.uow as uow:
            product_data = Product.model_validate(data)
            await uow.products.save(product_data)
            return product_data

    async def get_product(self, product_id: UUID) -> Product:
        async with self.uow as uow:
            product = await uow.products.get(product_id)
            if not product:
                raise NotFound("Product Not Found")

            return product

    async def delete_product(self, product_id: UUID) -> None:
        async with self.uow as uow:
            await uow.products.delete(product_id)

    async def get_product_by_title(self, title: str) -> Product:
        async with self.uow as uow:
            product = await uow.products.get_by_title(title)
            if not product:
                raise NotFound("Product Not Found")

            return product
