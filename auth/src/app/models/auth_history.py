from sqlalchemy_utils import IPAddressType, UUIDType

from app.storage.db import db

from .common import UUIDMixin


class AuthHistory(db.Model, UUIDMixin):  # type: ignore
    __tablename__ = 'auth_history'

    user_id = db.Column('user_id', UUIDType(binary=False),  # type: ignore
                        db.ForeignKey('users.id', ondelete='CASCADE'))  # type: ignore
    timestamp = db.Column(db.DateTime, server_default=db.func.now())  # type: ignore
    user_agent = db.Column(db.Text, nullable=False)  # type: ignore
    ip_address = db.Column(IPAddressType)  # type: ignore
    device = db.Column(db.Text, primary_key=True)  # type: ignore

    def __repr__(self):
        return '<User %s %d>' % (self.user_id, self.timestamp)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'user_agent': self.user_agent,
            'ip_address': str(self.ip_address),
            'device': self.device,
        }
