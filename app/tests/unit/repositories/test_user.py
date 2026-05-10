from app.domain import User

from ...fakes.fake_repositories import FakeUserRepository


class TestUser:
    # def __init__(self):
    #     self.repo = FakeUserRepository()

    async def test_add_user(self):
        repo = FakeUserRepository()
        user = User(
            first_name="Abdur",
            last_name="Rahim",
            email="abi@rahim.sheikh.com",
            hashed_password="ola",
        )
        response = await repo.save(user)
        assert response.id is not None
