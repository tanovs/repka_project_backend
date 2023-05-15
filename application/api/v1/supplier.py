from api.v1.schemas.supplier import (AddSupplierRequest, AddSupplierResponse,
                                     SupplierContacts, SupplierDeliveryInfo,
                                     SupplierDocuments)
from fastapi import APIRouter, Depends
from service.add_data_service import AddDataService, get_add_data_service
from service.get_data_service import GetDataService, get_data_service

router = APIRouter()


@router.post('/supplier/add', response_model=AddSupplierResponse)
async def add_supplier(
    supplier_data: AddSupplierRequest,
    data_service: AddDataService = Depends(get_add_data_service),
):
    supplier_id = await data_service.add_supplier(supplier_data)
    return AddSupplierResponse(
        status='success',
        message='supplier added',
        supplier_uuid=supplier_id,
    )


@router.get('/suppler/contacts/{supplier_id}', response_model=SupplierContacts)
async def supplier_contacts(
    supplier_id: str,
    data_service: GetDataService = Depends(get_data_service),
):
    contacts = await data_service.get_supplier_contacts(
        supplier_id=supplier_id,
    )
    return SupplierContacts.parse_obj(contacts)


@router.get('/supplier/delivery_info/{supplier_id}', response_model=SupplierDeliveryInfo)
async def supplier_delivery_info(
    supplier_id: str,
    data_service: GetDataService = Depends(get_data_service),
):
    delivery_info = await data_service.get_supplier_delivery_info(
        supplier_id=supplier_id,
    )
    return SupplierDeliveryInfo(
        delivery_day=delivery_info[0][0],
        delivery_time=delivery_info[0][1],
        min_price=delivery_info[0][2],
        city_name=[line[3] for line in delivery_info],
    )


@router.get('/suppler/documents/{supplier_id}', response_model=SupplierDocuments)
async def supplier_documents(
    supplier_id: str,
    data_service: GetDataService = Depends(get_data_service),
):
    documents = await data_service.get_supplier_documents(
        supplier_id=supplier_id,
    )
    return SupplierDocuments.parse_obj(documents)
