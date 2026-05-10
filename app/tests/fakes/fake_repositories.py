from uuid import uuid4

from ...domain import User
from ...interfaces.base_repository import BaseUserRepository


class FakeUserRepository(BaseUserRepository):
    def __init__(self):
        self.users: set[User] = set()

    async def save(self, data: User) -> User:
        if not data.id:
            data.id = uuid4()
        self.users.add(data)

    async def get(self, id) -> User:
        for user in self.users:
            if user.id == id:
                return user
        return None

    async def delete(self, id):
        for user in self.users:
            if user.id == id:
                self.users.remove(user)

    async def get_by_email(self, email) -> User:
        for user in self.users:
            if user.email == email:
                return user
        return None
