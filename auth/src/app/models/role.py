from enum import Enum

from marshmallow import EXCLUDE, validates
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy_utils import UUIDType

from app.storage.db import db

from .common import TimeStampedMixin, UUIDMixin


class DefaultRoleEnum(str, Enum):
    user = 'user'
    staff = 'staff'
    admin = 'admin'


class Role(db.Model, UUIDMixin, TimeStampedMixin):  # type: ignore

    __tablename__ = 'roles'

    name = db.Column(db.String(80), unique=True, nullable=False)  # type: ignore
    description = db.Column(db.Text, nullable=True)  # type: ignore

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<Role {self.name}>'

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    class Meta:
        PROTECTED_ROLE_NAMES = (
            DefaultRoleEnum.user.value,
            DefaultRoleEnum.staff.value,
            DefaultRoleEnum.admin.value,
        )


user_role = db.Table(  # type: ignore
    'user_role',
    db.Column('user_id', UUIDType(binary=False), db.ForeignKey('users.id', ondelete='CASCADE')),  # type: ignore
    db.Column('role_id', UUIDType(binary=False), db.ForeignKey('roles.id', ondelete='CASCADE')),  # type: ignore
    db.UniqueConstraint('user_id', 'role_id', name='uniq_user_role')  # type: ignore
)


class RoleSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Role
