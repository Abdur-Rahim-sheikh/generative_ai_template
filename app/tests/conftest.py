import pytest

from .fakes import FakeUnitOfWork
from ..services import BillingService


@pytest.fixture
def fake_uow() -> FakeUnitOfWork:
    return FakeUnitOfWork()


@pytest.fixture
def fake_billing_service() -> BillingService:
    return BillingService(uow=fake_uow)
