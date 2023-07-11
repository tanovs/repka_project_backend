import uuid
from dataclasses import dataclass

from db.postgresql import get_postgres
from fastapi import Depends
from models.supplier import City, Region, Supplier
from models.good import Good, Tag, Category
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker


@dataclass
class GetDataService:
    engine: AsyncEngine

    async def select_data(self, stmt: Select):
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            async with session.begin():
                ret = await session.execute(stmt)
                await session.commit()
                await session.flush()
                return ret
    
    async def get_region_service(self, region: str, size: int):
        if region:
            return (await self.select_data(stmt=(
                select(Region.id, Region.region_name)
                .order_by(Region.region_name)
                .where(Region.region_name > region)
                .limit(size)
            ))).fetchall()
        return (await self.select_data(stmt=(
            select(Region.id, Region.region_name)
            .order_by(Region.region_name)
            .limit(size)
        ))).fetchall()
    
    async def get_city_service(self):
        return (
            await self.select_data(
                stmt=(
                    select(City.id, City.city_name, Region.region_name)
                    .join(Region, Region.id == City.region_id)
                    .order_by(Region.region_name)
                )
            )
        ).fetchall()
    
    async def get_category_service(self, category: str, size: int):
        if category:
            return (await self.select_data(stmt=(
                select(Category.id, Category.category_name, Category.file_path)
                .order_by(Category.category_name)
                .where(Category.category_name > category)
                .limit(size)
            ))).fetchall()
        return (await self.select_data(stmt=(
            select(Category.id, Category.category_name, Category.file_path)
            .order_by(Category.category_name)
            .limit(size)
        ))).fetchall()
    
    async def get_tag_service(self, category: uuid.UUID, tag: str, size: int):
        if tag:
            return (await self.select_data(stmt=(
                select(Tag.id, Tag.tag_name)
                .order_by(Tag.tag_name)
                .where(Tag.category_id==category and Tag.tag_name > tag)
                .limit(size)
            ))).fetchall()
        return (await self.select_data(stmt=(
            select(Tag.id, Tag.tag_name)
            .order_by(Tag.tag_name)
            .where(Tag.category_id==category)
            .limit(size)
        ))).fetchall()

    # async def get_supplier_contacts(self, supplier_id: uuid.UUID):
    #     stmt = select(
    #         Supplier.contact_name,
    #         Supplier.company_address,
    #         Supplier.phone_number,
    #         Supplier.email,
    #         Supplier.website,
    #         Supplier.social_network,
    #     ).where(Supplier.id == supplier_id)
    #     ret = await self.select_data(stmt=stmt)
    #     return ret.fetchone()._asdict()

    # async def get_supplier_delivery_info(self, supplier_id: uuid.UUID):
    #     stmt = select(
    #         Supplier.delivery_day,
    #         Supplier.delivery_time,
    #         Supplier.min_price,
    #         City.city_name,
    #         Region.region_name,
    #     ).join(
    #         City, Supplier.delivery_city,
    #         ).where(Supplier.id == supplier_id).join(
    #         Region, Supplier.delivery_region,
    #         ).where(Supplier.id == supplier_id)
    #     ret = await self.select_data(stmt=stmt)
    #     return ret.fetchall()

    # async def get_supplier_documents(self, supplier_id: uuid.UUID):
    #     stmt = select(
    #         Supplier.OOO,
    #         Supplier.OGRN,
    #         Supplier.INN,
    #         Supplier.bank_account,
    #     ).where(Supplier.id==supplier_id)
    #     ret = await self.select_data(stmt=stmt)
    #     return ret.fetchone()._asdict()
    
    # async def get_good_by_category(self, category_id: uuid.UUID):
    #     stmt = (
    #         select(Good).
    #         join(Category).
    #         where(Category.id==category_id)
    #     )
    #     ret = await self.select_data(stmt=stmt)
    #     return ret


def get_data_service(
    engine: AsyncEngine = Depends(get_postgres),
) -> GetDataService:
    return GetDataService(engine=engine)
