import uuid

from api.v1.schemas.tags import (CategoriesResponse, CityTagResponse,
                                 RegionTagResponse, TagResponse)
from fastapi import APIRouter, Depends, Query
from service.get_data_service import GetDataService, get_data_service

router = APIRouter()


@router.get('/regions', response_model=RegionTagResponse)
async def get_regions(
    last_region: str = Query(default=None),
    size: int = Query(ge=1, le=100),
    data_service: GetDataService = Depends(get_data_service),
):
    regions = await data_service.get_region_service(region=last_region, size=size)
    return RegionTagResponse.parse_obj({'regions': regions})


@router.get('/cities', response_model=CityTagResponse)
async def get_cities(
    data_service: GetDataService = Depends(get_data_service),
):
    cities = await data_service.get_city_service()
    return CityTagResponse.parse_obj({'cities': cities})


@router.get('/category', response_model=CategoriesResponse)
async def get_categories(
    last_category: str = Query(default=None),
    size: int = Query(ge=1, le=100),
    data_service: GetDataService = Depends(get_data_service),
):
    categories = await data_service.get_category_service(category=last_category, size=size)
    return CategoriesResponse.parse_obj({'categories': categories})


@router.get('/good_tag/{category_id}', response_model=TagResponse)
async def get_good_tag(
    category_id: uuid.UUID,
    last_tag: str = Query(default=None),
    size: int = Query(ge=1, le=100),
    data_service: GetDataService = Depends(get_data_service),
):
    tags = await data_service.get_tag_service(category=category_id, tag=last_tag, size=size)
    return TagResponse.parse_obj({'tags': tags})
