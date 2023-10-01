from uuid import UUID

from pydantic import BaseModel
from typing import Optional


class RegionTag(BaseModel):
    id: UUID
    region_name: str

    class Config:
        orm_mode = True


class CityTag(BaseModel):
    id: UUID
    city_name: str
    region_name: str

    class Config:
        orm_mode = True


class RegionTagResponse(BaseModel):
    regions: list[RegionTag]

    class Config:
        orm_mode = True


class CityTagResponse(BaseModel):
    cities: list[CityTag]

    class Config:
        orm_mode = True


class Category(BaseModel):
    id: UUID
    category_name: str
    file_path: Optional[str]

    class Config:
        orm_mode = True


class CategoriesResponse(BaseModel):
    categories: list[Category]

    class Config:
        orm_mode = True


class GoodTag(BaseModel):
    id: UUID
    tag_name: str
    category_name: str

    class Config:
        orm_mode = True


class TagResponse(BaseModel):
    tags: list[GoodTag]

    class Config:
        orm_mode = True
