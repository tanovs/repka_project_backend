import uuid
from dataclasses import dataclass

from api.v1.schemas.good import AddGoodRequest
from api.v1.schemas.supplier import AddSupplierRequest, AddSupplierDeliveryLocation
from db.postgresql import get_postgres
from fastapi import Depends, UploadFile
from models.good import Good
from models.supplier import Supplier, SupplierCity, SupplierRegion
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker)
from typing import Optional
from sqlalchemy import Select, update


@dataclass
class UpdateDataService():
    engine: AsyncEngine

    async def get_session(self, stmt: Select) -> AsyncSession:
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            async with session.begin():
                ret = await session.execute(stmt)
                await session.commit()
                await session.flush()
                return ret
    
    async def add_supplier_files(
            self,
            supplier_id: uuid.UUID,
            cover: Optional[UploadFile] = None,
            logo: Optional[UploadFile] = None,
        ):
        if not cover:
            return (await self.get_session(
            stmt=(
                update(Supplier)
                .where(Supplier.id==supplier_id)
                .values(company_logo=logo)
                .returning(Supplier.id)
                )
            )).fetchone()
        if not logo:
            return (await self.get_session(
            stmt=(
                update(Supplier)
                .where(Supplier.id==supplier_id)
                .values(company_cover=cover)
                .returning(Supplier.id)
                )
            )).fetchone()
        return (await self.get_session(
            stmt=(
                update(Supplier)
                .where(Supplier.id==supplier_id)
                .values(company_cover=cover, company_logo=logo)
                .returning(Supplier.id)
            )
        )).fetchone()
    
    async def add_supplier_delivery_location(
            self,
            supplier_id: uuid.UUID,
            location: AddSupplierDeliveryLocation
    ):
        for region in location.delivery_regions:
            await self.get_session(
                SupplierRegion.insert().values(
                    supplier_id=supplier_id,
                    region_id=region
                )
            )
        for city in location.delivery_cities:
            await self.get_session(
                SupplierCity.insert().values(
                    supplier_id=supplier_id,
                    city_id=city
                )
            )
    
    async def add_good_photo(self, good_id: uuid.UUID, photo: UploadFile):
        return (await self.get_session(
            update(Good)
            .where(Good.id==good_id)
            .values(photo=photo)
            .returning(Good.id)
        )).fetchone()
        



def get_update_data_service(
    engine: AsyncEngine = Depends(get_postgres),
) -> UpdateDataService:
    return UpdateDataService(engine=engine)
