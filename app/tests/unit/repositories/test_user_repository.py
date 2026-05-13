import pytest

from ....domain.models import User
from ...fakes import FakeUserRepository
from .base import BaseRepositoryCommonTests


class TestUserRepository(BaseRepositoryCommonTests):
    @pytest.fixture
    def repo(self) -> FakeUserRepository:
        return FakeUserRepository()

    @pytest.fixture
    def sample_entity(self) -> User:
        return User(
            first_name="Abdur",
            last_name="Rahim",
            email="abdur@example.com",
            hashed_password="hashed_secret",
        )

    async def test_get_by_email_returns_matching_user(self, repo, sample_entity):
        await repo.save(sample_entity)
        fetched = await repo.get_by_email(sample_entity.email)
        assert fetched is not None
        assert fetched.email == sample_entity.email

    async def test_get_by_email_returns_none_for_unknown_email(self, repo):
        result = await repo.get_by_email("nobody@nowhere.com")
        assert result is None

    async def test_multiple_users_stored_independently(self, repo):
        u1 = User(
            first_name="Alice",
            last_name="A",
            email="alice@test.com",
            hashed_password="x",
        )
        u2 = User(
            first_name="Bob", last_name="B", email="bob@test.com", hashed_password="y"
        )
        await repo.save(u1)
        await repo.save(u2)
        assert await repo.get(u1.id) is u1
        assert await repo.get(u2.id) is u2
