from datetime import datetime, timezone
from typing import Annotated, Literal

from pydantic import EmailStr
from sqlmodel import UUID, Field, SQLModel

TimeStamp = Annotated[
    datetime, Field(default_factory=lambda: datetime.now(timezone.utc))
]


class User(SQLModel, table=True):
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    created_at: TimeStamp


class Product(SQLModel, table=True):
    title: str
    description: str
    price: float
    unit: Literal["second", "generation"]
    updated_at: TimeStamp


class Wallet(SQLModel, table=True):
    user_id: UUID
    coin_balance: int = 0
    free_uses_remaining: int = 3
    updated_at: Annotated[
        datetime,
        Field(
            default_factory=datetime.timezone.utc.now,
            sa_column_args={"onupdate": lambda: datetime.now(timezone.utc)},
        ),
    ]


class Transaction(SQLModel, table=True):
    wallet_id: UUID
    reference_id: UUID
    amount: int
    type: Literal["credit", "debit"]
    created_at: TimeStamp


class Session(SQLModel, table=True):
    user_id: UUID
    session_token: UUID = Field(default_factory=UUID, primary_key=True)
    created_at: TimeStamp
