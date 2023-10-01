from fastapi import APIRouter, Depends
from service.get_data_service import GetDataService, get_data_service
from typing import Optional
from datetime import datetime
from api.v1.schemas.search import AllSuppliers
from uuid import UUID


router = APIRouter()


@router.get('/supplier')
async def get_all_suppliers(
    limit: int,
    last_date: Optional[datetime] = None,
    service: GetDataService = Depends(get_data_service),
):
    data = await service.get_all_suppliers(limit=limit, last_date=last_date)
    return [AllSuppliers.parse_obj(supplier._asdict()) for supplier in data]


# @router.get('/search')
# async def search(
#     category_id: Optional[UUID] = None,
#     tag_id: Optional[UUID] = None,
#     city_id: Optional[UUID] = None,
#     region_id: Optional[UUID] = None,
#     service: GetDataService = Depends(get_data_service)
# ):
    