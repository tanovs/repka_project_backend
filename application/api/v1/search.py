from fastapi import APIRouter, Depends
from service.get_data_service import GetDataService, get_data_service
from typing import Optional
from datetime import datetime
from api.v1.schemas.search import AllSuppliers, MainScreenResponse, CompanyGoodsResponse, SearchWithParamsResponse, GoodSQLModel, GoodResponse, SearchGoodsResponse
from uuid import UUID
from typing import List


search_by_supplier = APIRouter()
search_by_good = APIRouter()
router_main_screen = APIRouter()


@router_main_screen.get('/')
async def get_main_screen_data(
    limit: int,
    last_company_name: Optional[str] = None,
    service: GetDataService = Depends(get_data_service),
):
    suppliers = await service.get_all_suppliers_and_goods(limit=limit, company_name=last_company_name)
    result_suppliers = []

    for supplier in suppliers:
        goods = []
        good = await service.get_supplier_goods(supplier_id=supplier._asdict()['id'], size=3, last_good_uuid=None)
        for item in good:
            res = CompanyGoodsResponse(
                good_id=item._asdict()['id'],
                name=item._asdict()['name'],
                volume=item._asdict()['volume'],
                price=item._asdict()['price'],
            )
            goods.append(res)
        supp = MainScreenResponse(
            company_id=supplier._asdict()['id'],
            company_name=supplier._asdict()['company_name'],
            company_goods=goods
        )
        result_suppliers.append(supp)
    return result_suppliers


@search_by_supplier.post('/supplier/search_with_params')
async def search_by_suppliers(
    like: Optional[str] = None,
    resp: Optional[SearchWithParamsResponse] = None,
    service: GetDataService = Depends(get_data_service),
):
    if not resp and not like:
        suppliers = await service.get_all_suppliers()
        return [AllSuppliers.parse_obj(supplier._asdict()) for supplier in suppliers]
    suppliers = await service.get_all_suppliers_by_params(params=resp, like=like)
    return [AllSuppliers.parse_obj(supplier._asdict()) for supplier in suppliers]


@search_by_good.post('/good/search_with_params')
async def search_by_goods(
    like: Optional[str] = None,
    resp: Optional[SearchWithParamsResponse] = None,
    service: GetDataService = Depends(get_data_service),
):
    response = []
    if not resp and not like:
        goods = await service.get_all_goods()
    else:
        goods = await service.get_all_goods_by_params(params=resp, like=like)
    print(goods)
    resp_dict = {}
    response = []
    for good in goods:
        supplier_with_good = GoodSQLModel.parse_obj(good._asdict())
        if not resp_dict.get(supplier_with_good.company_name):
            resp_dict[supplier_with_good.company_name] = []
        resp_dict[supplier_with_good.company_name].append(supplier_with_good)
    for key, val in resp_dict.items():
        goods = []
        for item in val:
            good = GoodResponse(
                id=item.good_id,
                name=item.name,
                volume=item.volume,
                price=item.price,
            )
            goods.append(good)
        response.append(
            SearchGoodsResponse(
                supplier_id=val[0].supplier_id,
                company_name=key,
                goods=goods,
            )
        )
            
    return response
    