import uuid

from api.v1.schemas.tags import (CategoriesResponse, CityTagResponse,
                                 RegionTagResponse, TagResponse)
from fastapi import APIRouter, Depends
from service.get_tags_service import GetTagsService, get_tags_service

router = APIRouter()


@router.get('/regions', response_model=RegionTagResponse)
async def get_regions(
    data_service: GetTagsService = Depends(get_tags_service),
):
    data_service.tag = 'region'
    regions = await data_service.get_tags()
    return RegionTagResponse.parse_obj({'regions': regions})


@router.get('/cities', response_model=CityTagResponse)
async def get_cities(
    data_service: GetTagsService = Depends(get_tags_service),
):
    data_service.tag = 'city'
    cities = await data_service.get_tags()
    return CityTagResponse.parse_obj({'cities': cities})


@router.get('/good_category', response_model=CategoriesResponse)
async def get_categories(
    data_service: GetTagsService = Depends(get_tags_service),
):
    data_service.tag = 'category'
    category = await data_service.get_tags()
    return CategoriesResponse.parse_obj({'categories': category})


@router.get('/good_tag/{category_id}', response_model=TagResponse)
async def get_good_tag(
    category_id: uuid.UUID,
    data_service: GetTagsService = Depends(get_tags_service),
):
    good_tag = await data_service.get_good_tag(category_id)
    return TagResponse.parse_obj({'good_tags': good_tag})
