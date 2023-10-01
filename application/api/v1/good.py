from uuid import UUID

from api.v1.schemas.good import AddGoodRequest, AddGoodResponse, GoodInfo
from fastapi import APIRouter, Depends, UploadFile, File
from service.add_data_service import AddDataService, get_add_data_service
from service.send_email_service import SendEmailService, get_send_email_service
from service.get_data_service import GetDataService, get_data_service
from service.update_data_service import UpdateDataService, get_update_data_service
from fastapi.responses import FileResponse

router = APIRouter()

@router.get('/good/template/download')
async def template_url():
    return 'https://docs.google.com/spreadsheets/d/1S9yu9PAivglJyTbMrRuj9cw5QUEkVVHlA7HyJbaw6ew/edit#gid=0'

@router.post('/good/template/upload/{supplier_id}')
async def send_notification(
    supplier_id: UUID,
    template: UploadFile | None = File(None),
    service: SendEmailService = Depends(get_send_email_service),
):
    await service.send_email_add_goods(
        content=template,
        supplier_id=supplier_id,
    )
    return {"status": "File send"}

@router.post('/good/add', response_model=AddGoodResponse)
async def add_good(
    request: AddGoodRequest,
    service: AddDataService = Depends(get_add_data_service),
):
    good_ids = await service.add_good(data=request)
    return AddGoodResponse(
        status='success',
        message='good added',
        good_uuid=good_ids,
    )

@router.post('/good/add/photo/{good_id}', response_model=AddGoodResponse)
async def add_good(
    good_id: UUID,
    photo: UploadFile = File(...),
    service: UpdateDataService = Depends(get_update_data_service),
):
    good_id = await service.add_good_photo(good_id=good_id, photo=photo.file.read())
    return AddGoodResponse(
        status='success',
        message='good added',
        good_uuid=good_id,
    )


@router.get('/good/information/{good_id}', response_model=GoodInfo)
async def good_information(
    good_id: UUID,
    service: GetDataService = Depends(get_data_service),
):
    good_info = await service.get_good_info(good_id=good_id)
    return GoodInfo.parse_obj(good_info)

# @router.get('/good/get_good_by_tag/{category_id}/{good_id}')
# async def get_good_by_tag(
#     category_id: uuid.UUID,
#     good_id: uuid.UUID = None,
#     service: GetDataService = Depends(get_data_service),
# ):
#     res = service.get_good_by_category(category_id=category_id)
#     print(res)
#     return "Ok"
