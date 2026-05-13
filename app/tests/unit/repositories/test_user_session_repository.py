from uuid import uuid4

import pytest

from ....domain.models import UserSession
from ...fakes import FakeUserSessionRepository
from .base import BaseRepositoryCommonTests


class TestUserSessionRepository(BaseRepositoryCommonTests):
    @pytest.fixture
    def repo(self) -> FakeUserSessionRepository:
        return FakeUserSessionRepository()

    @pytest.fixture
    def sample_entity(self) -> UserSession:
        return UserSession(user_id=uuid4())

    async def test_get_by_user_id(self, repo: FakeUserSessionRepository):
        user_id = uuid4()
        user_session = UserSession(
            user_id=user_id,
        )
        await repo.save(user_session)
        user_session2 = await repo.get_by_user_id(user_id=user_id)
        assert user_session2 == user_session
