from dataclasses import dataclass
from typing import Optional

from db.postgresql import get_postgres
from fastapi import Depends
from models.good import Category, Tag
from models.supplier import City, Region
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker


@dataclass
class GetTagsService:
    engine: AsyncEngine
    tag: Optional[str] = None

    async def select_tags(self, stmt: Select):
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            async with session.begin():
                ret = await session.execute(stmt)
                await session.commit()
                await session.flush()
                return ret.scalars().all()

    async def get_tags(self):
        tag_dict = {
            'region': Region,
            'city': City,
            'category': Category,
        }
        stmt = select(tag_dict[self.tag])
        return await self.select_tags(stmt)

    async def get_good_tag(self, category_id):
        stmt = select(Tag).where(Tag.category_id == category_id)
        return await self.select_tags(stmt)


def get_tags_service(
    engine: AsyncEngine = Depends(get_postgres),
) -> GetTagsService:
    return GetTagsService(engine=engine)
