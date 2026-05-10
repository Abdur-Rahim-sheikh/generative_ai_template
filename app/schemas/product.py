from typing import Literal

from pydantic import BaseModel, Field


class BaseProduct(BaseModel):
    title: str
    description: str
    coin_cost: int = Field(ge=0)
    unit: Literal["second", "generation"]


class CreateProductRequest(BaseProduct):
    pass
