import pytest
from uuid import uuid4

from ....domain import Product
from ...fakes import FakeProductRepository


@pytest.fixture
def repo() -> FakeProductRepository:
    return FakeProductRepository()


@pytest.fixture
def sample_product() -> Product:
    return Product(
        title="Image Generation",
        description="Generate stunning AI images",
        coin_cost=5,
        unit="generation",
    )


class TestFakeProductRepository:
    async def test_save_assigns_id(self, repo, sample_product):
        sample_product.id = None
        saved = await repo.save(sample_product)
        assert saved.id is not None

    async def test_save_ignores_existing_id(self, repo, sample_product):
        fixed_id = uuid4()
        sample_product.id = fixed_id
        saved = await repo.save(sample_product)
        assert saved.id != fixed_id

    async def test_get_returns_saved_product(self, repo, sample_product):
        saved = await repo.save(sample_product)
        fetched = await repo.get(saved.id)
        assert fetched == saved

    async def test_get_returns_none_for_unknown_id(self, repo):
        assert await repo.get(uuid4()) is None

    async def test_delete_removes_product(self, repo, sample_product):
        saved = await repo.save(sample_product)
        await repo.delete(saved.id)
        assert await repo.get(saved.id) is None

    async def test_delete_nonexistent_is_safe(self, repo):
        await repo.delete(uuid4())

    async def test_multiple_products_isolated(self, repo):
        p1 = Product(title="TTS", description="", price=0.01, unit="second")
        p2 = Product(title="Diffusion", description="", price=0.10, unit="generation")
        await repo.save(p1)
        await repo.save(p2)
        assert await repo.get(p1.id) is p1
        assert await repo.get(p2.id) is p2
