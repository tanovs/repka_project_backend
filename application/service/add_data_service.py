import uuid
from dataclasses import dataclass

from api.v1.schemas.good import AddGoodRequest
from api.v1.schemas.supplier import AddSupplierRequest
from db.postgresql import get_postgres
from fastapi import Depends
from models.good import Good
from models.supplier import Supplier, SupplierCity, SupplierRegion
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker)


@dataclass
class AddDataService():
    engine: AsyncEngine

    async def get_session(self) -> AsyncSession:
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            async with session.begin():
                yield session
                await session.commit()
                await session.flush()

    async def insert(self, data_obj: Supplier) -> uuid.UUID:
        session = self.get_session()
        async for add_session in session:
            add_session.add(data_obj)
            await add_session.commit()
            return data_obj.id

    async def insert_relative_data(self, relative_obj: list, table: str):
        location = {
            'Region': SupplierRegion,
            'City': SupplierCity,
        }
        session = self.get_session()
        async for add_session in session:
            await add_session.execute(
                insert(location[table]),
                relative_obj,
            )

    async def insert_supplier_data(self, req_params: AddSupplierRequest):
        supplier = Supplier(
            company_name=req_params.company_name,
            contact_name=req_params.contact_name,
            phone_number=req_params.phone_number,
            email=req_params.email,
            company_address=req_params.company_adress,
            website=req_params.website,
            social_network=req_params.social_network,
            delivery_time=req_params.delivery_time,
            delivery_day=req_params.delivery_day,
            min_price=req_params.min_price,
            OOO=req_params.OOO,
            OGRN=req_params.OGRN,
            INN=req_params.INN,
            bank_account=req_params.bank_account,
        )
        return await self.insert(supplier)

    async def insert_good_data(
        self,
        req_params: AddGoodRequest,
        supplier_id: uuid.UUID,
    ):
        good = Good(
            supplier_id=supplier_id,
            name=req_params.name,
            # photo=req_params.photo,
            price=req_params.price,
            volume=req_params.volume,
            limit=req_params.limit,
            calories=req_params.calories,
            compound=req_params.compound,
            expiration_day=req_params.expiration_day,
        )
        return await self.insert(good)

    async def generate_location(
        self,
        ids: list,
        table: str,
        supplier_id: uuid,
    ):
        location = {
            'Region': 'region_id',
            'City': 'city_id',
        }
        bulk_location = []
        for item_id in ids:
            bulk_location.append({
                'supplier_id': supplier_id,
                location[table]: item_id,
            })
        await self.insert_relative_data(bulk_location, table)

    async def add_supplier(self, req_params: AddSupplierRequest):
        supplier_id = await self.insert_supplier_data(params=req_params)
        # await self.generate_location(
        # params.delivery_region, 'Region', supplier_id)
        await self.generate_location(
            req_params.delivery_city,
            'City',
            supplier_id,
        )
        # if params.certificate:
        #     certs = []
        #     for cert_params in params:
        #         certs.append(Certificate(
        # photo=cert_params.photo, url=cert_params.url))
        return supplier_id

    async def add_good(self, req_params: AddGoodRequest):
        good_ids = []
        for good in req_params.goods:
            good_id = await self.insert_good_data(
                params=good,
                supplier_id=req_params.supplier_id,
            )
            good_ids.append(good_id)
        # add_categories
        # add_tags
        return good_ids


def get_add_data_service(
    engine: AsyncEngine = Depends(get_postgres),
) -> AddDataService:
    return AddDataService(engine=engine)
