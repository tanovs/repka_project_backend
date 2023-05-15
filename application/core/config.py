import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

load_dotenv()


class PostgreSettings(BaseSettings):
    password: str = os.getenv('POSTGRES_PASSWORD')
    host: str = os.getenv('POSTGRES_HOST')
    port: str = os.getenv('POSTGRES_PORT')
    database: str = os.getenv('POSTGRES_DB')
    user: str = os.getenv('POSTGRES_USER')
    url: str = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}'
    alembic_url: str = f'postgresql://{user}:{password}@{host}:{port}/{database}'


class MailSettings(BaseSettings):
    mail_user: str = os.getenv('MAIL_USERNAME')
    password: str = os.getenv('MAIL_PASSWORD')
    port: str = os.getenv('MAIL_PORT')
    server: str = os.getenv('MAIL_SERVER')
    mail_from: str = os.getenv('MAIL_FROM')
    mail_from_name: str = os.getenv('MAIL_FROM_NAME')


class Settings(BaseSettings):
    db: PostgreSettings = PostgreSettings()
    mail: MailSettings = MailSettings()
