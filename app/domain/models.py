from datetime import datetime, timezone
from typing import Annotated, Literal
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlmodel import Field, SQLModel, String

TimeStamp = Annotated[
    datetime, Field(default_factory=lambda: datetime.now(timezone.utc))
]
PrimaryKey = Annotated[UUID | None, Field(default_factory=uuid4, primary_key=True)]


class User(SQLModel, table=True):
    id: PrimaryKey
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    created_at: TimeStamp

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Product(SQLModel, table=True):
    id: PrimaryKey
    title: str
    description: str
    price: float
    unit: Literal["second", "generation"] = Field(sa_type=String)
    updated_at: TimeStamp


class Wallet(SQLModel, table=True):
    id: PrimaryKey
    user_id: UUID = Field(foreign_key="user.id", unique=True)
    coin_balance: int = 0
    free_uses_remaining: int = 3
    updated_at: Annotated[
        datetime,
        Field(
            default_factory=lambda: datetime.now(timezone.utc),
            sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
        ),
    ]


class Transaction(SQLModel, table=True):
    id: PrimaryKey
    wallet_id: UUID = Field(foreign_key="wallet.id")
    reference_id: UUID | None = Field(foreign_key="product.id", nullable=True)
    amount: int
    type: Literal["credit", "debit"] = Field(sa_type=String)
    created_at: TimeStamp


class Session(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", unique=True)
    session_token: UUID = Field(default_factory=UUID, primary_key=True)
    created_at: TimeStamp
