import uuid

from api.v1.schemas.good import AddGoodRequest, AddGoodResponse
from fastapi import APIRouter, Depends, UploadFile
from service.add_data_service import AddDataService, get_add_data_service
from service.send_email_service import SendEmailService, get_send_email_service

router = APIRouter()


@router.post('/good/add', response_model=AddGoodResponse)
async def add_good(
    request: AddGoodRequest,
    service: AddDataService = Depends(get_add_data_service),
):
    good_ids = await service.add_good(params=request)
    return AddGoodResponse(
        status='success',
        message='good added',
        good_uuid=good_ids,
    )


@router.post('/good/upload_file/{supplier_id}')
async def upload_file(
    supplier_id: uuid.UUID,
    file_content: UploadFile,
    service: SendEmailService = Depends(get_send_email_service),
):
    await service.send_email(
        file_content=file_content,
        supplier_id=supplier_id,
    )
    return {'filename': file_content.filename}
