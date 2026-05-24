from datetime import datetime, timezone
from typing import Annotated, Literal
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlmodel import TIMESTAMP, Field, SQLModel, String, Relationship
from sqlalchemy import CheckConstraint

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
    wallet: "Wallet" = Relationship(back_populates="user", cascade_delete=True)
    user_session: "UserSession" = Relationship(
        back_populates="user", cascade_delete=True
    )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Product(SQLModel, table=True):
    id: PrimaryKey
    title: str = Field(unique=True)
    description: str = Field(default="")
    coin_cost: int = Field(ge=0, sa_column_args=(CheckConstraint("coin_cost >= 0")))
    unit: Literal["second", "generation"] = Field(sa_type=String)
    updated_at: TimeStampUpdate

    transactions: list["Transaction"] = Relationship(back_populates="product")


class Wallet(SQLModel, table=True):
    id: PrimaryKey
    user_id: UUID | None = Field(
        foreign_key="user.id", unique=True, nullable=False, ondelete="CASCADE"
    )
    coin_balance: int = Field(
        default=0, ge=0, sa_column_args=(CheckConstraint("coin_balance >= 0"),)
    )
    free_uses_remaining: int = Field(
        default=0, ge=0, sa_column_args=(CheckConstraint("free_uses_remaining >= 0"),)
    )
    updated_at: TimeStampUpdate
    user: User = Relationship(back_populates="wallet")

    transactions: list["Transaction"] = Relationship(
        back_populates="wallet", cascade_delete=True
    )


class Transaction(SQLModel, table=True):
    id: PrimaryKey
    wallet_id: UUID | None = Field(
        foreign_key="wallet.id", nullable=False, ondelete="CASCADE"
    )
    product_id: UUID | None = Field(foreign_key="product.id", nullable=True)
    amount: int = Field(ge=0, sa_column_args=(CheckConstraint("amount>=0"),))
    type: Literal["credit", "debit"] = Field(sa_type=String)
    created_at: TimeStamp

    wallet: Wallet = Relationship(back_populates="transactions")
    product: Product = Relationship(back_populates="transactions")


class UserSession(SQLModel, table=True):
    id: PrimaryKey

    user_id: UUID | None = Field(
        foreign_key="user.id", index=True, nullable=False, ondelete="CASCADE"
    )
    expires_at: datetime = Field(sa_type=TIMESTAMP(timezone=True))

    user: User = Relationship(back_populates="user_session")
