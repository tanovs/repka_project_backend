import uuid

from api.v1.schemas.tags import (CategoriesResponse, CityTagResponse,
                                 RegionTagResponse, TagResponse)
from fastapi import APIRouter, Depends, Query
from service.get_data_service import GetDataService, get_data_service
from typing import Optional


router = APIRouter()


@router.get('/regions/all', response_model=RegionTagResponse, description='Метод возвращает все регионы')
async def get_regions_all(
    last_region: str = Query(default=None),
    size: int = Query(ge=1, le=100),
    data_service: GetDataService = Depends(get_data_service),
):
    regions = await data_service.get_region_service(region=last_region, size=size)
    return RegionTagResponse.parse_obj({'regions': regions})


@router.get('/regions/like', response_model=RegionTagResponse, description='Метод возвращает регионы название которых начинается с like="..."')
async def get_regions_like(
    like: str = None,
    data_service: GetDataService = Depends(get_data_service),
):
    regions = await data_service.get_region_service_like(like=like)
    return RegionTagResponse.parse_obj({'regions': regions})


@router.get('/cities/all', response_model=CityTagResponse, description='Метод возвращает все города')
async def get_cities_all(
    data_service: GetDataService = Depends(get_data_service),
):
    cities = await data_service.get_city_service()
    return CityTagResponse.parse_obj({'cities': cities})


@router.get('/cities', response_model=CityTagResponse, description='Метод возвращает все города, которые есть в регионе')
async def get_cities_by_region(
    region_id: uuid.UUID,
    data_service: GetDataService = Depends(get_data_service),
):
    cities = await data_service.get_city_service_in_region(region=region_id)
    return CityTagResponse.parse_obj({'cities': cities})

@router.get('/cities/like', response_model=CityTagResponse, description='Метод возвращает все города название которых начинается с like="..."')
async def get_cities_like(
    like: str,
    data_service: GetDataService = Depends(get_data_service),
):
    cities = await data_service.get_city_service_like(like=like)
    return CityTagResponse.parse_obj({'cities': cities})


@router.get('/category/all', response_model=CategoriesResponse, description='Метод возвращает все категории')
async def get_categories_all(
    last_category: str = Query(default=None),
    size: int = Query(ge=1, le=100),
    data_service: GetDataService = Depends(get_data_service),
):
    categories = await data_service.get_category_service(category=last_category, size=size)
    return CategoriesResponse.parse_obj({'categories': categories})


@router.get('/category/like', response_model=CategoriesResponse, description='Метод возвращает все категории название которых начинается с like="..."')
async def get_categories_like(
    like: str,
    data_service: GetDataService = Depends(get_data_service),
):
    categories = await data_service.get_category_service_like(like=like)
    return CategoriesResponse.parse_obj({'categories': categories})


@router.get('/good_tag/all', response_model=TagResponse, description='Метод, который возвращает все тэги')
async def get_good_tag_all(
    last_tag: str = Query(default=None),
    size: int = Query(ge=1, le=100),
    data_service: GetDataService = Depends(get_data_service),
):
    tags = await data_service.get_tag_service_all(tag=last_tag, size=size)
    return TagResponse.parse_obj({'tags': tags})


@router.get('/good_tag/like', response_model=TagResponse, description='Метод, который возвращает все тэги название которых начинается с like="..."')
async def get_good_tag_like(
    like: str,
    data_service: GetDataService = Depends(get_data_service),
):
    tags = await data_service.get_tag_service_like(like=like)
    return TagResponse.parse_obj({'tags': tags})


@router.get('/good_tag/{category_id}', response_model=TagResponse, description='Метод возвращает все тэги, которые есть в категории')
async def get_good_tag_category(
    category_id: uuid.UUID,
    data_service: GetDataService = Depends(get_data_service),
):
    tags = await data_service.get_tag_service(category=category_id)
    return TagResponse.parse_obj({'tags': tags})


@router.get('/good_tag/{category_id}/like', response_model=TagResponse, description='Метод возвращает все тэги, которые есть в категории название которых начинается с like="..."')
async def get_good_tag_category_like(
    like: str,
    category_id: uuid.UUID,
    data_service: GetDataService = Depends(get_data_service),
):
    tags = await data_service.get_tag_service_category_like(category=category_id, like=like)
    return TagResponse.parse_obj({'tags': tags})
