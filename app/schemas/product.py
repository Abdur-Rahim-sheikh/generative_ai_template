from typing import Literal

from pydantic import BaseModel


class BaseProduct(BaseModel):
    title: str
    description: str
    price: float
    unit: Literal["second", "generation"]


class CreateProductRequest(BaseProduct):
    pass
