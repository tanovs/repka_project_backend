from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class AddGood(BaseModel):
    name: str
    price: str
    volume: str
    balance: str
    calories: Optional[str]
    compound: Optional[str]
    expiration_day: Optional[str]
    producer: Optional[str]
    sample: Optional[bool]
    sample_amount: Optional[int]
    tag_id: str

    class Config:
        orm_mode = True


class AddGoodRequest(BaseModel):
    supplier_id: UUID
    goods: list[AddGood]

    class Config:
        orm_mode = True