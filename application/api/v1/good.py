from uuid import UUID

from api.v1.schemas.good import AddGoodRequest, AddGoodResponse, GoodInfo, AddGoodPhotoResponse
from fastapi import APIRouter, Depends, UploadFile, File, Response
from service.add_data_service import AddDataService, get_add_data_service
from service.send_email_service import SendEmailService, get_send_email_service
from service.get_data_service import GetDataService, get_data_service
from service.update_data_service import UpdateDataService, get_update_data_service
from fastapi.responses import FileResponse


router_add = APIRouter()
router_get = APIRouter()


@router_add.post('/good/add', response_model=AddGoodResponse)
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

@router_add.post('/good/add/photo/{good_id}', response_model=AddGoodPhotoResponse)
async def add_good(
    good_id: UUID,
    photo: UploadFile = File(...),
    service: UpdateDataService = Depends(get_update_data_service),
):
    good_id = await service.add_good_photo(good_id=good_id, photo=photo.file.read())
    return AddGoodPhotoResponse(
        status='success',
        message='good added',
        good_uuid=good_id[0],
    )


@router_get.get('/good/information/{good_id}', response_model=GoodInfo)
async def good_information(
    good_id: UUID,
    service: GetDataService = Depends(get_data_service),
):
    good_info = await service.get_good_info(good_id=good_id)
    return GoodInfo.parse_obj(good_info)
 
@router_get.get('/good/photo/{good_id}')
async def get_good_photo(
    good_id: UUID,
    service: GetDataService = Depends(get_data_service),
):
    good_photo = await service.get_good_photo(good_id=good_id)
    return Response(content=good_photo[0], media_type='application/octet-stream')