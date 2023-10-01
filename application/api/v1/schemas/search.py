from pydantic import BaseModel
from uuid import UUID

class AllSuppliers(BaseModel):
    id: UUID
    company_name: str
    estimated_delivery_time: str
    min_price: str