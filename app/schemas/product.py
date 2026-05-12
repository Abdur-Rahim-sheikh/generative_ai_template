from typing import Literal

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class BaseProduct(BaseModel):
    title: str
    description: str
    coin_cost: int = Field(ge=0)
    unit: Literal["second", "generation"]


class CreateProductRequest(BaseProduct):
    pass


class ReadProduct(BaseProduct):
    id: UUID
    updated_at: datetime
