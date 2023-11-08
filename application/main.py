import uvicorn
from api.v1 import good, supplier, tags, orders, search
from core.config import Settings
from db import postgresql
from fastapi import FastAPI
from fastapi_mail import ConnectionConfig
from mail import mail
from sqlalchemy.ext.asyncio import create_async_engine

SETTINGS = Settings()

PROJECT_NAME = 'repka'

app = FastAPI(
    title=f'Read-only API for ({PROJECT_NAME}).',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
)

@app.on_event('startup')
async def startup():
    postgresql.postgres = create_async_engine(SETTINGS.db.url, echo=True)
    mail.mail = ConnectionConfig(
        MAIL_USERNAME=SETTINGS.mail.mail_user,
        MAIL_PASSWORD=SETTINGS.mail.password,
        MAIL_FROM=SETTINGS.mail.mail_from,
        MAIL_PORT=SETTINGS.mail.port,
        MAIL_SERVER=SETTINGS.mail.server,
        MAIL_FROM_NAME=SETTINGS.mail.mail_from_name,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        MAIL_DEBUG=True,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=False,
    )


@app.on_event('shutdown')
async def shutdown():
    await postgresql.postgres.dispose()

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(
# request: Request, exc: RequestValidationError):
#     details = exc.errors()
#     return JSONResponse(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         content=AddSupplierResponse(
# status='false', message=details[0]["msg"]).json(),
#     )

app.include_router(tags.router, prefix='/api/v1', tags=['Ручки для получения городов, регионов, категорий и тэгов'])

app.include_router(supplier.router_supplier_add, prefix='/api/v1', tags=['Ручки для экрана "Форма для поставщиков"'])
app.include_router(good.router_add, prefix='/api/v1', tags=['Ручки для экрана "Форма для поставщиков"'])

app.include_router(supplier.router_supplier_get, prefix='/api/v1', tags=['Ручки для экрана "Экран поставщика"'])
app.include_router(good.router_get, prefix='/api/v1', tags=['Ручки для экрана "Экран товара"'])

app.include_router(orders.router, prefix='/api/v1', tags=['Ручки для экрана "Сценарий заказа товара"'])

app.include_router(search.router_main_screen, prefix='/api/v1', tags=['Ручки для экрана "Главный экран + поиск"'])
app.include_router(search.search_by_supplier, prefix='/api/v1', tags=['Ручки для экрана "Главный экран + поиск (поиск по поставщикам)"'])
app.include_router(search.search_by_good, prefix='/api/v1', tags=['Ручки для экрана "Главный экран + поиск (поиск по товарам)"'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080)
