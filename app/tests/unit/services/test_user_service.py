from uuid import uuid4

import pytest

from ....schemas.user import CreateUserRequest
from ....services.user_service import UserService
from ...fakes import FakeUnitOfWork
from ....domain.exceptions import NotFound


@pytest.fixture
def user_service(fake_uow: FakeUnitOfWork) -> UserService:
    return UserService(uow=fake_uow)


@pytest.fixture
def create_request() -> CreateUserRequest:
    return CreateUserRequest(
        first_name="Nadia",
        last_name="Islam",
        email="nadia@example.com",
        password="securepassword123",
    )


@pytest.mark.slow
class TestUserService:
    async def test_create_user_returns_user_with_id(
        self, user_service: UserService, create_request: CreateUserRequest
    ):
        user = await user_service.create_user(create_request)
        assert user is not None
        assert user.id is not None

    async def test_create_user_stores_correct_fields(
        self, user_service: UserService, create_request: CreateUserRequest
    ):
        user = await user_service.create_user(create_request)
        assert user.first_name == create_request.first_name
        assert user.last_name == create_request.last_name
        assert user.email == create_request.email

    async def test_create_user_hashes_password(
        self, user_service: UserService, create_request: CreateUserRequest
    ):
        user = await user_service.create_user(create_request)
        # raw password must NOT appear in the stored hash
        assert create_request.password.get_secret_value() not in user.hashed_password

    async def test_create_user_commits_uow(
        self,
        user_service: UserService,
        create_request: CreateUserRequest,
        fake_uow: FakeUnitOfWork,
    ):
        await user_service.create_user(create_request)
        assert fake_uow.committed is True

    async def test_get_user_returns_existing_user(
        self, user_service: UserService, create_request: CreateUserRequest
    ):
        created = await user_service.create_user(create_request)
        fetched = await user_service.get_user(created.id)
        assert fetched is not None
        assert fetched.id == created.id

    async def test_get_user_returns_notfound_exception_for_missing_id(
        self, user_service
    ):
        with pytest.raises(NotFound):
            await user_service.get_user(uuid4())

    async def test_delete_user_removes_from_storage(
        self, user_service: UserService, create_request: CreateUserRequest
    ):
        created = await user_service.create_user(create_request)
        await user_service.delete_user(created.id)
        # directly inspect the fake repo to confirm deletion
        assert await user_service.uow.users.get(created.id) is None

    async def test_get_user_by_email_returns_correct_user(
        self, user_service: UserService, create_request: CreateUserRequest
    ):
        created = await user_service.create_user(create_request)
        fetched = await user_service.get_user_by_email(create_request.email)
        assert fetched is not None
        assert fetched.id == created.id

    async def test_get_user_by_email_returns_notfound_exception_for_unknown(
        self, user_service: UserService
    ):
        with pytest.raises(NotFound):
            await user_service.get_user_by_email("ghost@nowhere.com")

    async def test_rollback_called_on_exception(self, fake_uow: FakeUnitOfWork):
        """If the service raises inside the context, rollback must be called."""

        class BrokenRepo:
            async def save(self, data):
                raise RuntimeError("DB exploded")

            async def get(self, id):
                return None

            async def delete(self, id):
                pass

            async def get_by_email(self, email):
                return None

        fake_uow.users = BrokenRepo()
        service = UserService(uow=fake_uow)
        with pytest.raises(RuntimeError):
            await service.create_user(
                CreateUserRequest(
                    first_name="X",
                    last_name="Y",
                    email="x@y.com",
                    password="pw",
                )
            )
        assert fake_uow.rolled_back is True
