import pytest
from uuid import uuid4

from ....domain.models import User
from ...fakes import FakeUserRepository


@pytest.fixture
def repo() -> FakeUserRepository:
    return FakeUserRepository()


@pytest.fixture
def sample_user() -> User:
    return User(
        first_name="Abdur",
        last_name="Rahim",
        email="abdur@example.com",
        hashed_password="hashed_secret",
    )


class TestFakeUserRepository:
    async def test_save_assigns_id(self, repo, sample_user):
        """A user without an id gets one assigned on save."""
        sample_user.id = None
        saved = await repo.save(sample_user)
        assert saved.id is not None

    async def test_save_ignores_existing_id(self, repo, sample_user):
        """If the user already has an id, save must not overwrite it."""
        existing_id = uuid4()
        sample_user.id = existing_id
        saved = await repo.save(sample_user)
        assert saved.id is not None and saved.id != existing_id

    async def test_save_returns_the_same_user_object(self, repo, sample_user):
        saved = await repo.save(sample_user)
        assert saved is sample_user

    async def test_get_returns_saved_user(self, repo, sample_user):
        saved = await repo.save(sample_user)
        fetched = await repo.get(saved.id)
        assert fetched == saved

    async def test_get_returns_none_for_unknown_id(self, repo):
        result = await repo.get(uuid4())
        assert result is None

    async def test_delete_removes_user(self, repo, sample_user):
        saved = await repo.save(sample_user)
        await repo.delete(saved.id)
        fetched = await repo.get(saved.id)
        assert fetched is None

    async def test_delete_nonexistent_id_is_safe(self, repo):
        """Deleting an id that does not exist must not raise."""
        await repo.delete(uuid4())  # no exception expected

    async def test_get_by_email_returns_matching_user(self, repo, sample_user):
        await repo.save(sample_user)
        fetched = await repo.get_by_email(sample_user.email)
        assert fetched is not None
        assert fetched.email == sample_user.email

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
