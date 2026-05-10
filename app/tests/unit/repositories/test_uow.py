import pytest

from ...fakes import FakeUnitOfWork


@pytest.fixture
def uow() -> FakeUnitOfWork:
    return FakeUnitOfWork()


class TestFakeUnitOfWork:
    async def test_commit_is_called_on_clean_exit(self, uow):

        async with uow:
            pass
        assert uow.committed is True
        assert uow.rolled_back is False

    async def test_rollback_is_called_on_exception(self, uow):

        with pytest.raises(RuntimeError):
            async with uow:
                raise RuntimeError("boom")
        assert uow.rolled_back is True
        assert uow.committed is False

    async def test_flags_reset_on_reuse(self, uow):

        async with uow:
            pass
        assert uow.committed is True

        # second use — flags should reset
        async with uow:
            pass
        assert uow.committed is True
        assert uow.rolled_back is False

    async def test_users_repo_is_accessible(self, uow):

        async with uow as ctx:
            assert ctx.users is not None

    async def test_products_repo_is_accessible(self, uow):

        async with uow as ctx:
            assert ctx.products is not None
