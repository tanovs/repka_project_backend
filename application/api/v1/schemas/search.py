from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class CompanyGoodsResponse(BaseModel):
    good_id: UUID
    name: str
    volume: str
    price: str

class MainScreenResponse(BaseModel):
    company_id: UUID
    company_name: str
    company_goods: List[CompanyGoodsResponse]

class AllSuppliers(BaseModel):
    id: UUID
    company_name: str
    estimated_delivery_time: str
    min_price: str


class SearchWithParamsResponse(BaseModel):
    category_id: Optional[List[UUID]] = None
    tag_id: Optional[List[UUID]] = None
    city_id: Optional[List[UUID]] = None
    region_id: Optional[List[UUID]] = None


class GoodResponse(BaseModel):
    id: UUID
    name: str
    volume: str
    price: str


class SearchGoodsResponse(BaseModel):
    supplier_id: UUID
    company_name: str
    goods: List[GoodResponse]


class GoodSQLModel(BaseModel):
    supplier_id: UUID
    company_name: str
    good_id: UUID
    name: str
    volume: str
    price: str