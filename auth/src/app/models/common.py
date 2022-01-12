import datetime
import uuid

from sqlalchemy_utils import UUIDType

from app.storage.db import db


class UUIDMixin:
    id = db.Column(  # type: ignore
        UUIDType(binary=False),
        primary_key=True,
        default=uuid.uuid4
    )


class TimeStampedMixin:
    created_at = db.Column(db.DateTime,  # type: ignore
                           nullable=False,
                           default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime,  # type: ignore
                           nullable=False,
                           default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow)
