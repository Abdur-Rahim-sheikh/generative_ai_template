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
            saved = await uow.products.save(product_data)
            return saved

    async def get_product(self, product_id: UUID) -> Product:
        async with self.uow as uow:
            product = await uow.products.get(product_id)
            if not product:
                raise NotFound("Product Not Found")

            return product

    async def delete_user(self, product_id: UUID) -> None:
        async with self.uow as uow:
            await uow.products.delete(product_id)
