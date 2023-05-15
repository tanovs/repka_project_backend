from typing import Optional
from uuid import UUID

from pydantic import BaseModel


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
    company_adress: str
    website: Optional[str] = None
    social_network: Optional[str] = None
    delivery_region: Optional[list[UUID]] = None
    delivery_city: Optional[list[UUID]] = None
    delivery_time: Optional[str] = None
    delivery_day: Optional[str] = None
    min_price: Optional[str] = None
    OOO: Optional[str] = None
    OGRN: Optional[str] = None
    INN: Optional[str] = None
    bank_account: Optional[str] = None
    certificate: Optional[list[Certificate]] = None


class SupplierContacts(BaseModel):
    contact_name: str
    company_address: str
    phone_number: str
    email: str
    website: str
    social_network: str


class SupplierDeliveryInfo(BaseModel):
    city_name: list[str]
    delivery_day: str
    delivery_time: str
    min_price: str


class SupplierDocuments(BaseModel):
    OOO: str
    OGRN: str
    INN: str
    bank_account: str
