from datetime import datetime, timezone
from typing import Annotated, Literal
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlmodel import TIMESTAMP, Field, SQLModel, String, Relationship

TimeStamp = Annotated[
    datetime,
    Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=TIMESTAMP(timezone=True),
    ),
]

TimeStampUpdate = Annotated[
    datetime,
    Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc),
        },
    ),
]

PrimaryKey = Annotated[UUID | None, Field(default_factory=uuid4, primary_key=True)]


class User(SQLModel, table=True):
    id: PrimaryKey
    first_name: str
    last_name: str
    email: EmailStr = Field(unique=True)
    hashed_password: str
    is_active: bool = True
    created_at: TimeStamp
    wallet: "Wallet" = Relationship(back_populates="user")
    user_session: "UserSession" = Relationship(back_populates="user")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Product(SQLModel, table=True):
    id: PrimaryKey
    title: str = Field(unique=True)
    description: str = Field(default="")
    coin_cost: int = Field(ge=0)
    unit: Literal["second", "generation"] = Field(sa_type=String)
    updated_at: TimeStamp

    transactions: list["Transaction"] = Relationship(back_populates="product")


class Wallet(SQLModel, table=True):
    id: PrimaryKey
    user_id: UUID = Field(foreign_key="user.id", unique=True, ondelete="CASCADE")
    coin_balance: int = Field(default=0, ge=0)
    free_uses_remaining: int = Field(default=0, ge=0)
    updated_at: TimeStampUpdate
    user: User = Relationship(back_populates="wallet", cascade_delete=True)

    transactions: list["Transaction"] = Relationship(back_populates="wallet")


class Transaction(SQLModel, table=True):
    id: PrimaryKey
    wallet_id: UUID = Field(foreign_key="wallet.id", ondelete="CASCADE")
    reference_id: UUID | None = Field(
        foreign_key="product.id", nullable=True, ondelete="CASCADE"
    )
    amount: int = Field(ge=0)
    type: Literal["credit", "debit"] = Field(sa_type=String)
    created_at: TimeStamp

    wallet: Wallet = Relationship(back_populates="transactions", cascade_delete=True)
    product: Product = Relationship(back_populates="transactions", cascade_delete=True)


class UserSession(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", unique=True, ondelete="CASCADE")
    session_token: UUID = Field(default_factory=UUID, primary_key=True)

    last_activity_at: TimeStampUpdate
    expires_at: datetime = Field(sa_type=TIMESTAMP(timezone=True))

    user: User = Relationship(back_populates="user_session", cascade_delete=True)
