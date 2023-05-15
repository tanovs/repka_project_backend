from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class AddGood(BaseModel):
    name: str
    photo: Optional[bytes]
    price: str
    limit: str
    volume: str
    calories: str
    compound: str
    expiration_day: str
    category: list[str]
    tag: list[str]


class AddGoodRequest(BaseModel):
    supplier_id: UUID
    goods: list[AddGood]


class AddGoodResponse(BaseModel):
    status: str
    message: str
    good_uuid: list[UUID]
