import pytest

from ....domain.models import Product
from ...fakes import FakeProductRepository
from .base import BaseRepositoryCommonTests


class TestProductRepository(BaseRepositoryCommonTests):
    @pytest.fixture
    def repo(self) -> FakeProductRepository:
        return FakeProductRepository()

    @pytest.fixture
    def sample_entity(self) -> Product:
        return Product(
            title="Image Generation",
            description="Generate stunning AI images",
            coin_cost=5,
            unit="generation",
        )

    async def test_multiple_products_isolated(self, repo):
        p1 = Product(title="TTS", description="", coin_cost=2, unit="second")
        p2 = Product(title="Diffusion", description="", coin_cost=3, unit="generation")
        await repo.save(p1)
        await repo.save(p2)
        assert await repo.get(p1.id) is p1
        assert await repo.get(p2.id) is p2
