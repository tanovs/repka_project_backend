from fastapi import APIRouter, Depends
from api.v1.schemas.order import OrderRequest
from service.send_email_service import SendEmailService, get_send_email_service
from service.add_data_service import AddDataService, get_add_data_service

router = APIRouter()


@router.post('/order')
async def make_order(
    req: OrderRequest,
    add_service: AddDataService = Depends(get_add_data_service),
    email_service: SendEmailService = Depends(get_send_email_service)
):
    info_id = await add_service.add_order_info(req)
    # email_service.send_email_horeca()
    for order in req.supplier_goods:
        await add_service.add_bucket(order, info_id)
        # email_service.send_email_supplier()
    return "OK"
    