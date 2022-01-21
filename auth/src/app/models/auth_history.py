from app.logging import get_logger
from app.storage.db import db
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import IPAddressType, UUIDType
from user_agents import parse

from .common import UUIDMixin
from .user import User


class AuthHistory(db.Model, UUIDMixin):  # type: ignore
    __tablename__ = 'auth_history_master'
    __table_args__ = (
        {
            'postgresql_partition_by': 'LIST (device)'
        }
    )

    user_id = db.Column('user_id', UUIDType(binary=False),  # type: ignore
                        db.ForeignKey('users_master.id', ondelete='CASCADE'))  # type: ignore
    timestamp = db.Column(db.DateTime, server_default=db.func.now())  # type: ignore
    user_agent = db.Column(db.Text, nullable=False)  # type: ignore
    ip_address = db.Column(IPAddressType)  # type: ignore
    device = db.Column(db.Text, primary_key=True)  # type: ignore

    def __repr__(self):
        return '<User %s %d>' % (self.user_id, self.timestamp)

    @staticmethod
    def user_agent_to_user_device(ua_string) -> str:
        user_agent = parse(ua_string)
        if user_agent.is_mobile:
            device = 'mobile'
        elif (
            not user_agent.is_pc and 'smart' in str(user_agent.device.model).lower() or 'smart-tv' in ua_string.lower()
        ):
            device = 'smart'
        else:
            device = 'web'
        return device

    @staticmethod
    def add_auth_history(user: User) -> None:
        ip_address = request.remote_addr
        user_agent = request.user_agent.string

        auth_history = AuthHistory(
            user_id=user.id,
            user_agent=user_agent,
            ip_address=ip_address,
            device=AuthHistory.user_agent_to_user_device(user_agent)
        )
        db.session.add(auth_history)
        try:
            db.session.commit()
        except SQLAlchemyError as exception:
            get_logger().error(f'Ошибка записи истории аутентификаций {str(exception)}')

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'user_agent': self.user_agent,
            'ip_address': str(self.ip_address),
            'device': self.device,
        }
