import uvicorn
from api.v1 import good, supplier, tags
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

app.include_router(supplier.router, prefix='/api/v1', tags=['supplier'])
app.include_router(good.router, prefix='/api/v1', tags=['good'])
app.include_router(tags.router, prefix='/api/v1', tags=['tags'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)