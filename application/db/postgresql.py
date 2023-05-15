from typing import Optional

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base

postgres: Optional[AsyncEngine] = None

meta = MetaData('repka')
Base = declarative_base(metadata=meta)


def get_postgres() -> AsyncEngine:
    return postgres


def get_base():
    return Base
