import uuid
from dataclasses import dataclass

from api.v1.schemas.good import AddGoodRequest
from api.v1.schemas.supplier import AddSupplierRequest, AddSupplierDeliveryLocation
from api.v1.schemas.order import SupplierGoodDeliveryInfo, OrderRequest
from db.postgresql import get_postgres
from fastapi import Depends, UploadFile
from models.good import Good
from models.order import Bucket, Order
from models.supplier import Supplier, SupplierCity, SupplierRegion, SupplierCert
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker)
from typing import Optional


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

    async def add_supplier(self, data: AddSupplierRequest):
        return await self.insert(Supplier(**data.dict()))

    async def add_supplier_certs(
        self,
        supplier_id: uuid,
        url: Optional[str] = None,
        cert: Optional[UploadFile] = None,
    ):
        if not url:
            return await self.insert(
                SupplierCert(
                    certificate=cert,
                    supplier_id=supplier_id
                )
            )
        if not cert:
            return await self.insert(
                SupplierCert(
                    certificate_url=url,
                    supplier_id=supplier_id
                )
            )
        return await self.insert(
            SupplierCert(
                certificate=cert,
                certificate_url=url,
                supplier_id=supplier_id
            )
        )
    
    async def add_good(self, data: AddGoodRequest):
        good_ids = []
        for val in data.goods:
            good_id = await self.insert(Good(**val.dict(), supplier_id=data.supplier_id))
            good_ids.append(good_id)
        return good_ids
    
    async def add_order_info(self, data: OrderRequest):
        return await self.insert(Order(
            company_name=data.company_name,
            delivery_city_region=data.delivery_city_region,
            delivery_adress=data.delivery_adress,
            contact_name=data.contact_name,
            contact_phone=data.contact_phone,
            contact_email=data.contact_email,
            ooo=data.ooo,
            inn=data.inn,
            bank_account=data.bank_account,
            bank_name=data.bank_name,
        ))
    
    async def add_bucket(self, data: SupplierGoodDeliveryInfo, info_id: uuid.UUID) -> list:
        bucket_ids = []
        for good in data.goods_id:
            bucket_id = await self.insert(Bucket(**good.dict(), supplier_id=data.supplier_id, info_id=info_id))
            bucket_ids.append(bucket_id)
        return bucket_ids


def get_add_data_service(
    engine: AsyncEngine = Depends(get_postgres),
) -> AddDataService:
    return AddDataService(engine=engine)
