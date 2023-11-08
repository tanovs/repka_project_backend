import uuid
from dataclasses import dataclass

from db.postgresql import get_postgres
from fastapi import Depends
from models.supplier import City, Region, Supplier, SupplierCity, SupplierRegion
from models.good import Good, Tag, Category
from sqlalchemy import Select, select, or_
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from typing import Optional
from datetime import datetime


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

    async def get_region_service_like(self, like: str):
        return (await self.select_data(stmt=(
            select(Region.id, Region.region_name)
            .order_by(Region.region_name)
            ).filter(Region.region_name.ilike(f'%{like}%'))
        )).fetchall()
    
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
    
    async def get_city_service_in_region(self, region: uuid.UUID):
        return (
            await self.select_data(
                stmt=(
                    select(City.id, City.city_name, Region.region_name)
                    .join(Region, Region.id == City.region_id)
                    .where(Region.id == region)
                    .order_by(Region.region_name)
                )
            )
        ).fetchall()
    
    async def get_city_service_like(self, like: str):
        return (
            await self.select_data(
                stmt=(
                    select(City.id, City.city_name, Region.region_name)
                    .join(Region, Region.id == City.region_id)
                    .order_by(Region.region_name)
                ).filter(City.city_name.ilike(f'%{like}%'))
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
    
    async def get_category_service_like(self, like: str):
        return (
            await self.select_data(
                stmt=(
                    select(Category.id, Category.category_name, Category.file_path)
                    .order_by(Category.category_name)
                ).filter(Category.category_name.ilike(f'%{like}%'))
            )
        ).fetchall()
    
    async def get_tag_service(self, category: uuid.UUID):
        return (
            await self.select_data(
                stmt=(
                    select(Tag.id, Tag.tag_name, Category.category_name)
                    .join(Category, Category.id==Tag.category_id)
                    .where(Category.id == category)
                    .order_by(Tag.tag_name)
                )
            )
        ).fetchall()
    
    async def get_tag_service_category_like(self, category: uuid.UUID, like: str):
        return (
            await self.select_data(
                stmt=(
                    select(Tag.id, Tag.tag_name, Category.category_name)
                    .join(Category, Category.id==Tag.category_id)
                    .where(Category.id == category)
                ).filter(Tag.tag_name.ilike(f'%{like}%'))
            )
        ).fetchall()
    
    async def get_tag_service_all(self, size: int, tag: str = None):
        if tag:
            return (
                await self.select_data(
                    stmt=(
                        select(Tag.id, Tag.tag_name, Category.category_name)
                        .join(Category, Category.id == Tag.category_id)
                        .order_by(Tag.tag_name)
                        .where(Tag.tag_name > tag)
                        .limit(size)
                    )
                )
            ).fetchall()
        return (
                await self.select_data(
                    stmt=(
                        select(Tag.id, Tag.tag_name, Category.category_name)
                        .join(Category, Category.id == Tag.category_id)
                        .order_by(Tag.tag_name)
                        .limit(size)
                    )
                )
            ).fetchall()
    
    async def get_tag_service_like(self, like: str):
        return (
                await self.select_data(
                    stmt=(
                        select(Tag.id, Tag.tag_name, Category.category_name)
                        .join(Category, Category.id == Tag.category_id)
                        .order_by(Tag.tag_name)
                    ).filter(Tag.tag_name.ilike(f'%{like}%'))
                )
            ).fetchall()
    
    
    async def get_supplier_data_for_email_service(self, supplier_id: uuid.UUID):
        return (
            await self.select_data(
                stmt=(
                    select(Supplier.company_name, Supplier.email)
                    .where(Supplier.id==supplier_id)
                )
            )
        ).fetchall()
    
    async def get_supplier_company_name(self, supplier_id: uuid.UUID):
        return (
            await self.select_data(
                stmt=(
                    select(Supplier.company_name, Supplier.orders_day_time)
                    .where(Supplier.id==supplier_id)
                )
            )
        ).fetchone()._asdict()

    async def get_supplier_contacts(self, supplier_id: uuid.UUID):
        stmt = select(
            Supplier.contact_name,
            Supplier.company_adress,
            Supplier.phone_number,
            Supplier.email,
            Supplier.website,
            Supplier.social_network,
        ).where(Supplier.id == supplier_id)
        ret = await self.select_data(stmt=stmt)
        return ret.fetchone()._asdict()

    async def get_supplier_delivery_info(self, supplier_id: uuid.UUID):
        stmt = select(
            City.city_name,
            Region.region_name,
            Supplier.delivery_day_time,
            Supplier.min_price,
            Supplier.estimated_delivery_time,
        ).join(
            City, Supplier.delivery_city,
            ).join(
            Region, Supplier.delivery_region,
            ).where(Supplier.id == supplier_id)
        ret = await self.select_data(stmt=stmt)
        return ret.fetchall()

    async def get_region_for_supplier(self, supplier_id: uuid.UUID):
        return (await self.select_data(
            stmt = select(
                Region.region_name
            ).join(
                Region, Supplier.delivery_region,
            ).where(Supplier.id == supplier_id)
        )).fetchall()
    
    async def get_city_for_supplier(self, supplier_id: uuid.UUID):
        return (await self.select_data(
            stmt = select(
                City.city_name
            ).join(
                City, Supplier.delivery_city,
            ).where(Supplier.id == supplier_id)
        )).fetchall()

    async def get_supplier_documents(self, supplier_id: uuid.UUID):
        stmt = select(
            Supplier.ooo,
            Supplier.ogrn,
            Supplier.inn,
        ).where(Supplier.id==supplier_id)
        ret = await self.select_data(stmt=stmt)
        return ret.fetchone()._asdict()
    
    async def get_supplier_goods(self, supplier_id: uuid.UUID, size: int, last_good_uuid: Optional[uuid.UUID]):
        if last_good_uuid:
            return (await self.select_data(
                stmt = select(
                Good.id,
                Good.name,
                Good.volume,
                Good.price,
            ).order_by(Good.name)
            .where(Good.supplier_id == supplier_id, Good.id > last_good_uuid)
            .limit(size))).fetchall()
        return (await self.select_data(
                stmt = select(
                Good.id,
                Good.name,
                Good.volume,
                Good.price,
            ).order_by(Good.name)
            .where(Good.supplier_id == supplier_id)
            .limit(size))).fetchall()
    
    async def get_good_info(self, good_id: uuid.UUID):
        return (await self.select_data(
            stmt=select(
                Good.name,
                Good.price,
                Good.volume,
                Good.balance,
                Good.calories,
                Good.compound,
                Good.expiration_day,
                Good.producer,
                Good.sample,
                Good.sample_amount,
            ).where(Good.id==good_id)
        )).fetchone()._asdict()
    
    async def get_supplier_tag(self, supplier_id: uuid.UUID):
        return (
            await self.select_data(
                stmt = select(Tag.tag_name, Tag.id)
                .join(Good)
                .where(Good.supplier_id == supplier_id)
            )
        ).fetchall()
    
    async def get_good_by_category(self, supplier_id: uuid.UUID, tags_id: list[uuid.UUID]):
        return (
            await self.select_data(
                stmt=select(
                    Good.id,
                    Good.name,
                    Good.price,
                    Good.volume
                )
                .where(Good.supplier_id==supplier_id, Good.tag_id.in_(tags_id))
                .order_by(Good.tag_id)
            )
        ).fetchall()
    
    async def get_all_suppliers(self):
        stmt = select(
            Supplier.id,
            Supplier.company_name,
            Supplier.estimated_delivery_time,
            Supplier.min_price,
        ).order_by(Supplier.company_name)
        
        return (await self.select_data(stmt=stmt)).fetchall()

    
    async def get_supplier_logo(self, supplier_id: uuid.UUID):
        return (
            await self.select_data(
                stmt=select(Supplier.company_logo).where(Supplier.id==supplier_id)
            )
        ).fetchone()
    
    async def get_supplier_cover(self, supplier_id: uuid.UUID):
        return (
            await self.select_data(
                stmt=select(Supplier.company_cover).where(Supplier.id==supplier_id)
            )
        ).fetchone()
    
    async def get_good_photo(self, good_id: uuid.UUID):
        return (
            await self.select_data(
                stmt=select(Good.photo).where(Good.id==good_id)
            )
        ).fetchone()
    
    async def get_all_suppliers_and_goods(self, limit: int, company_name: Optional[str] = None):
        if not company_name:
            stmt = select(Supplier.id, Supplier.company_name).limit(limit)
        else:
            stmt = select(Supplier.id, Supplier.company_name).where(Supplier.company_name > company_name).limit(limit)
        suppliers = (await self.select_data(stmt=stmt)).fetchall()
        return suppliers
    
    async def get_all_suppliers_by_params(self, like: str = None, params = None):
        stmt = (
            select(Supplier.id, Supplier.company_name, Supplier.estimated_delivery_time, Supplier.min_price)
            .join(Good, Good.supplier_id==Supplier.id)
            .join(Tag, Good.tag_id==Tag.id)
            .join(Category, Tag.category_id==Category.id)
            .join(SupplierRegion, SupplierRegion.supplier_id==Supplier.id)
            .join(Region, Region.id==SupplierRegion.region_id)
            .join(SupplierCity, SupplierCity.supplier_id==Supplier.id)
            .join(City, City.id==SupplierCity.city_id)
        )
        if params:
            if params.category_id:
                stmt = stmt.filter(Category.id.in_(params.category_id))
            if params.tag_id:
                stmt = stmt.filter(Tag.id.in_(params.tag_id))
            if params.city_id:
                stmt = stmt.filter(City.id.in_(params.city_id))
            if params.region_id:
                stmt = stmt.filter(Region.id.in_(params.region_id))
        if like:
            stmt = stmt.filter(or_(Supplier.company_name.ilike(f'%{like}%'),
                               Tag.tag_name.ilike(f'%{like}%'),
                               Category.category_name.ilike(f'%{like}%')))
        stmt = stmt.order_by(Supplier.company_name)
        suppliers = (await self.select_data(stmt=stmt))
        return suppliers.fetchall()
    
    async def get_all_goods(self):
        stmt = select(
            Supplier.id.label('supplier_id'),
            Supplier.company_name,
            Good.id.label('good_id'),
            Good.name,
            Good.volume,
            Good.price,
        ).join(Good, Good.supplier_id==Supplier.id).order_by(Supplier.company_name)
        
        return (await self.select_data(stmt=stmt)).fetchall()
    
    async def get_all_goods_by_params(self, like: str = None, params = None):
        stmt = (
            select(Supplier.id.label('supplier_id'), Supplier.company_name, Good.id.label('good_id'), Good.name, Good.volume, Good.price)
            .join(Good, Good.supplier_id==Supplier.id)
            .join(Tag, Good.tag_id==Tag.id)
            .join(Category, Tag.category_id==Category.id)
            .join(SupplierRegion, SupplierRegion.supplier_id==Supplier.id)
            .join(Region, Region.id==SupplierRegion.region_id)
            .join(SupplierCity, SupplierCity.supplier_id==Supplier.id)
            .join(City, City.id==SupplierCity.city_id)
        )
        if params:
            if params.category_id:
                stmt = stmt.filter(Category.id.in_(params.category_id))
            if params.tag_id:
                stmt = stmt.filter(Tag.id.in_(params.tag_id))
            if params.city_id:
                stmt = stmt.filter(City.id.in_(params.city_id))
            if params.region_id:
                stmt = stmt.filter(Region.id.in_(params.region_id))
        if like:
            stmt = stmt.filter(or_(Good.name.ilike(f'%{like}%'),
                                   Good.compound.ilike(f'%{like}%'),
                                   Tag.tag_name.ilike(f'%{like}%'),
                                   Category.category_name.ilike(f'%{like}%')))
        stmt = stmt.order_by(Supplier.company_name)
        goods = (await self.select_data(stmt=stmt))
        return goods.fetchall()


def get_data_service(
    engine: AsyncEngine = Depends(get_postgres),
) -> GetDataService:
    return GetDataService(engine=engine)
