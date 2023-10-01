from typing import List
from uuid import UUID

from pydantic import BaseModel


class GoodDeliveryInfo(BaseModel):
    good_id: UUID
    amount: int


class SupplierGoodDeliveryInfo(BaseModel):
    supplier_id: UUID
    goods_id: List[GoodDeliveryInfo]


class OrderRequest(BaseModel):
    company_name: str
    delivery_city_region: str
    delivery_adress: str
    contact_name: str
    contact_phone: str
    contact_email: str
    ooo: str
    inn: str
    bank_account: str
    bank_name: str
    supplier_goods: List[SupplierGoodDeliveryInfo]
