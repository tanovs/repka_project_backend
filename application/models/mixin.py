import uuid
from datetime import datetime

import sqlalchemy.dialects.postgresql as postgresql
from sqlalchemy import Column, DateTime


class UUIDMixin(object):
    id = Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
        unique=True,
    )


class TimeStampMixin(object):
    created = Column(
        DateTime(timezone=True),
        default=datetime.now(),
        nullable=False,
    )
    modified = Column(
        DateTime(timezone=True),
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False,
    )
