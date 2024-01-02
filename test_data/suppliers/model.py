from pydantic import BaseModel
from typing import Optional

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