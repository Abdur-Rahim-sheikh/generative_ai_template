import pytest
from uuid import uuid4

from ....schemas.product import CreateProductRequest
from ....services.product_service import ProductService
from ...fakes import FakeUnitOfWork


@pytest.fixture
def uow() -> FakeUnitOfWork:
    return FakeUnitOfWork()


@pytest.fixture
def service(uow) -> ProductService:
    return ProductService(uow=uow)


@pytest.fixture
def create_request() -> CreateProductRequest:
    return CreateProductRequest(
        title="AI Voiceover",
        description="High quality TTS generation",
        coin_cost=4,
        unit="second",
    )


class TestProductService:
    async def test_create_product_returns_product_with_id(
        self, service, create_request
    ):
        product = await service.create_product(create_request)
        assert product is not None
        assert product.id is not None

    async def test_create_product_persists_title(self, service, create_request, uow):
        assert uow == service.uow, "Both unit of work are not same"
        product = await service.create_product(create_request)
        fetched = await uow.products.get(product.id)
        assert fetched is not None
        assert fetched.title == create_request.title

    async def test_create_product_commits_uow(self, service, create_request, uow):
        await service.create_product(create_request)
        assert uow.committed is True

    async def test_get_product_returns_existing(self, service, create_request):
        created = await service.create_product(create_request)
        fetched = await service.get_product(created.id)
        assert fetched is not None
        assert fetched.id == created.id

    async def test_get_product_returns_none_for_missing(self, service):
        result = await service.get_product(uuid4())
        assert result is None

    async def test_delete_product_removes_from_storage(
        self, service, create_request, uow
    ):
        created = await service.create_product(create_request)
        await service.delete_user(created.id)
        assert await uow.products.get(created.id) is None

    async def test_coin_cost_is_stored_correctly(self, service, create_request):
        product = await service.create_product(create_request)
        assert product.coin_cost == create_request.coin_cost

    async def test_unit_is_stored_correctly(self, service, create_request):
        product = await service.create_product(create_request)
        assert product.unit == create_request.unit
