from typing import Annotated, Optional
from uuid import UUID

from api.v1.schemas.supplier import (AddSupplierDeliveryLocation,
                                     AddSupplierRequest, AddSupplierResponse,
                                     GetSuppliersGoodResponse,
                                     SupplierContacts, SupplierDeliveryInfo,
                                     SupplierDocuments, SupplierGoodInfo,
                                     SupplierInfo, SupplierTagResponse, SupplierGoodInfoResponse)
from fastapi import APIRouter, Body, Depends, File, Form, Response, UploadFile
from service.add_data_service import AddDataService, get_add_data_service
from service.get_data_service import GetDataService, get_data_service
from service.send_email_service import SendEmailService, get_send_email_service
from service.update_data_service import (UpdateDataService,
                                         get_update_data_service)

router_supplier_add = APIRouter()
router_supplier_get = APIRouter()


# Добавление поставщика
@router_supplier_add.post('/supplier/add', response_model=AddSupplierResponse)
async def add_supplier(
    supplier_data: AddSupplierRequest,
    data_service: AddDataService = Depends(get_add_data_service),
):
    supplier_id = await data_service.add_supplier(data=supplier_data)
    return AddSupplierResponse(
        status='success',
        message='supplier added',
        supplier_uuid=supplier_id,
    )

@router_supplier_add.post('/supplier/add/files/{supplier_id}', response_model=AddSupplierResponse)
async def add_supplier_files(
    supplier_id: UUID,
    company_cover: UploadFile | None = File(None),
    company_logo: UploadFile | None = File(None),
    data_service: UpdateDataService = Depends(get_update_data_service),
):
    if company_cover and company_logo:
        supplier_id = await data_service.add_supplier_files(
            supplier_id=supplier_id,
            cover=company_cover.file.read(),
            logo=company_logo.file.read(),
        )
    elif not company_logo:
        supplier_id = await data_service.add_supplier_files(
            supplier_id=supplier_id,
            cover=company_cover.file.read(),
        )
    elif not company_cover:
        supplier_id = await data_service.add_supplier_files(
            supplier_id=supplier_id,
            logo=company_logo.file.read(),
        )
    return AddSupplierResponse(
        status='success',
        message='files added',
        supplier_uuid=supplier_id[0],
    )

@router_supplier_add.post('/supplier/add/delivery_location/{supplier_id}', response_model=AddSupplierResponse)
async def add_supplier_region_city(
    supplier_id: UUID,
    location: AddSupplierDeliveryLocation,
    data_service: UpdateDataService = Depends(get_update_data_service),
):
    await data_service.add_supplier_delivery_location(
        supplier_id=supplier_id,
        location=location,
    )
    return AddSupplierResponse(
        status='success',
        message='location added',
        supplier_uuid=supplier_id,
    )

@router_supplier_add.post('/supplier/add/certs/{supplier_id}', response_model=AddSupplierResponse)
async def add_supplier_certs(
    supplier_id: UUID,
    cert_url: Optional[str] = None,
    cert: UploadFile | None = File(None),
    data_service: AddDataService = Depends(get_add_data_service),
):
    if not cert:
        supplier_id = await data_service.add_supplier_certs(
            supplier_id=supplier_id,
            url=cert_url,
        )
    elif not cert_url:
        supplier_id = await data_service.add_supplier_certs(
            supplier_id=supplier_id,
            cert=cert.file.read(),
        )
    elif cert and cert_url:
        supplier_id = await data_service.add_supplier_certs(
            supplier_id=supplier_id,
            url=cert_url,
            cert=cert.file.read(),
        )
    return AddSupplierResponse(
        status='success',
        message='certs added',
        supplier_uuid=supplier_id,
    )

@router_supplier_add.post('/supplier/send_notification/{supplier_id}', response_model=AddSupplierResponse)
async def send_notification(
    supplier_id: UUID,
    profile_url: str,
    service: SendEmailService = Depends(get_send_email_service),
    db_service: GetDataService = Depends(get_data_service)
):
    info = await db_service.get_supplier_data_for_email_service(supplier_id=supplier_id)
    await service.send_email_add_supplier(company_name=info[0].company_name, url=profile_url, email=info[0].email)
    return AddSupplierResponse(
        status='success',
        message='notification send',
        supplier_uuid=supplier_id,
    )
    

# Получение данных о поставщике
@router_supplier_get.get('/supplier/company_name/{supplier_id}', response_model=SupplierInfo)
async def get_supplier_company_name(
    supplier_id: UUID,
    service: GetDataService = Depends(get_data_service)
):
    company_name = await service.get_supplier_company_name(supplier_id=supplier_id)
    return SupplierInfo.parse_obj(company_name)

@router_supplier_get.get('/supplier/logo/{supplier_id}')
async def get_supplier_logo(
    supplier_id: UUID,
    service: GetDataService = Depends(get_data_service),
):
    logo = await service.get_supplier_logo(supplier_id=supplier_id)
    return Response(content=logo[0], media_type='application/octet-stream')

@router_supplier_get.get('/supplier/cover/{supplier_id}')
async def get_supplier_cover(
    supplier_id: UUID,
    service: GetDataService = Depends(get_data_service),
):
    cover = await service.get_supplier_cover(supplier_id=supplier_id)
    return Response(content=cover[0], media_type='application/octet-stream')

@router_supplier_get.get('/suppler/contacts/{supplier_id}', response_model=SupplierContacts)
async def supplier_contacts(
    supplier_id: UUID,
    data_service: GetDataService = Depends(get_data_service),
):
    contacts = await data_service.get_supplier_contacts(
        supplier_id=supplier_id,
    )
    return SupplierContacts.parse_obj(contacts)


@router_supplier_get.get('/supplier/delivery_info/{supplier_id}', response_model=SupplierDeliveryInfo)
async def supplier_delivery_info(
    supplier_id: UUID,
    data_service: GetDataService = Depends(get_data_service),
):
    delivery_info = await data_service.get_supplier_delivery_info(
        supplier_id=supplier_id,
    )
    delivery_region_info = await data_service.get_region_for_supplier(
        supplier_id=supplier_id,
    )
    delivery_city_info = await data_service.get_city_for_supplier(
        supplier_id=supplier_id,
    )
    return SupplierDeliveryInfo(
        city_name = [city.city_name for city in delivery_city_info],
        region_name = [region.region_name for region in delivery_region_info],
        delivery_day_time = delivery_info[0].delivery_day_time,
        min_price = delivery_info[0].min_price,
        estimated_delivery_time = delivery_info[0].estimated_delivery_time
    )


@router_supplier_get.get('/suppler/documents/{supplier_id}', response_model=SupplierDocuments)
async def supplier_documents(
    supplier_id: UUID,
    data_service: GetDataService = Depends(get_data_service),
):
    documents = await data_service.get_supplier_documents(
        supplier_id=supplier_id,
    )
    return SupplierDocuments.parse_obj(documents)

@router_supplier_get.get('/supplier/good/{supplier_id}', response_model=list[SupplierGoodInfo])
async def supplier_good(
    supplier_id: UUID,
    size: int,
    last_good_uuid: Optional[UUID] = None,
    data_service: GetDataService = Depends(get_data_service)
):
    supplier_good = await data_service.get_supplier_goods(
        supplier_id=supplier_id,
        size=size,
        last_good_uuid=last_good_uuid
    )
    return [SupplierGoodInfo.parse_obj(good._asdict()) for good in supplier_good]

@router_supplier_get.get('/supplier/tag/{supplier_id}')
async def supplier_categories(
    supplier_id: UUID,
    service: GetDataService = Depends(get_data_service),
):
    supplier_tags = await service.get_supplier_tag(supplier_id=supplier_id)
    supplier_tags_models = []
    tag_names = []
    for item in supplier_tags:
        tag_name = (item._asdict())['tag_name']
        if tag_name not in tag_names:
            model = SupplierTagResponse(
                id=(item._asdict())['id'],
                tag_name=(item._asdict())['tag_name'],
            )
            supplier_tags_models.append(model)
            tag_names.append(tag_name)
    return supplier_tags_models

@router_supplier_get.post('/supplier/good/category/{supplier_id}')
async def get_supplier_good_by_tag(
    supplier_id: UUID,
    list_tags: GetSuppliersGoodResponse = ...,
    service: GetDataService = Depends(get_data_service),
):
    goods = await service.get_good_by_category(
        supplier_id=supplier_id,
        tags_id = list_tags.tag_id,
    )
    result = []
    for good in goods:
        result_good = SupplierGoodInfoResponse(
            id=(good._asdict())['id'],
            name=(good._asdict())['name'],
            price=(good._asdict())['price'],
            volume=(good._asdict())['volume'],
        )
        result.append(result_good)
    return result