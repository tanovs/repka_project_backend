from typing import Optional
from uuid import UUID

from pydantic import BaseModel
import json


class AddSupplierResponse(BaseModel):
    status: str
    message: str
    supplier_uuid: UUID


class Certificate(BaseModel):
    photo: Optional[bytes] = None
    url: Optional[str] = None


class AddSupplierRequest(BaseModel):
    company_name: str
    contact_name: str
    phone_number: str
    email: str
    company_adress: Optional[str]
    website: Optional[str] = None
    social_network: Optional[str] = None
    delivery_day_time: str
    estimated_delivery_time: str
    min_price: str
    orders_day_time: str
    ooo: str
    ogrn: str
    inn: str

    class Config:
        orm_mode = True

class AddSupplierDeliveryLocation(BaseModel):
    delivery_regions: list[UUID]
    delivery_cities: list[UUID]

class SupplierContacts(BaseModel):
    contact_name: str
    company_adress: str
    phone_number: str
    email: str
    website: Optional[str]
    social_network: Optional[str]


class SupplierDeliveryInfo(BaseModel):
    city_name: list[str]
    region_name: list[str]
    delivery_day_time: str
    min_price: str
    estimated_delivery_time: str



class SupplierDocuments(BaseModel):
    ooo: str
    ogrn: str
    inn: str


class SupplierInfo(BaseModel):
    company_name: str
    orders_day_time: str

    class Config:
        orm_mode = True

class SupplierGoodInfo(BaseModel):
    id: UUID
    name: str
    volume: str
    price: str

class GetSuppliersGoodResponse(BaseModel):
    tag_id: list[UUID]

class SupplierTagResponse(BaseModel):
    id: UUID
    tag_name: str


class SupplierGoodInfoResponse(BaseModel):
    id: UUID
    name: str
    price: str
    volume: str