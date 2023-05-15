import uuid
from dataclasses import dataclass

from db.postgresql import get_postgres
from fastapi import Depends
from models.supplier import City, Region, Supplier
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

    async def get_supplier_contacts(self, supplier_id: uuid.UUID):
        stmt = select(
            Supplier.contact_name,
            Supplier.company_address,
            Supplier.phone_number,
            Supplier.email,
            Supplier.website,
            Supplier.social_network,
        ).where(Supplier.id == supplier_id)
        ret = await self.select_data(stmt=stmt)
        return ret.fetchone()._asdict()

    async def get_supplier_delivery_info(self, supplier_id: uuid.UUID):
        stmt = select(
            Supplier.delivery_day,
            Supplier.delivery_time,
            Supplier.min_price,
            City.city_name,
            Region.region_name,
        ).join(
            City, Supplier.delivery_city,
            ).where(Supplier.id == supplier_id).join(
            Region, Supplier.delivery_region,
            ).where(Supplier.id == supplier_id)
        ret = await self.select_data(stmt=stmt)
        return ret.fetchall()

    async def get_supplier_documents(self, supplier_id: uuid.UUID):
        stmt = select(
            Supplier.OOO,
            Supplier.OGRN,
            Supplier.INN,
            Supplier.bank_account,
        )
        ret = await self.select_data(stmt=stmt)
        return ret.fetchone()._asdict()


def get_data_service(
    engine: AsyncEngine = Depends(get_postgres),
) -> GetDataService:
    return GetDataService(engine=engine)
