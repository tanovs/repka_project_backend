import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, UUID, Column, MetaData
from sqlalchemy.orm import declarative_base

meta = MetaData(schema='content')
Base = declarative_base(metadata=meta)


class UUIDMixin(object):
    id = Column(
        'id',
        UUID,
        primary_key=True,
        nullable=False,
        default=uuid.uuid4(),
    )


class TimeStampMixin(object):
    created = Column(
        'created',
        TIMESTAMP,
        nullable=False,
        default=datetime.now(),
    )
    modified = Column(
        'modified',
        TIMESTAMP,
        nullable=False,
        onupdate=datetime.now(),
    )
