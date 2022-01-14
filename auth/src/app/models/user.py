from app.exceptions import ModelSchemaValidationException
from app.logging import get_logger
from app.models.role import Role
from app.storage.db import db
from marshmallow import EXCLUDE, validates
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy_utils import UUIDType
from werkzeug.security import check_password_hash, generate_password_hash

from .common import TimeStampedMixin, UUIDMixin
from .role import user_role


class User(db.Model, TimeStampedMixin, UUIDMixin):  # type: ignore
    __tablename__ = 'users_master'
    __table_args__ = (
        {
            'postgresql_partition_by': 'HASH (id)'
        }
    )

    login = db.Column(db.String(250), unique=True, nullable=False)  # type: ignore
    _password_hash = db.Column('password', db.String, nullable=False)  # type: ignore
    first_name = db.Column(db.String(250), nullable=True)  # type: ignore
    last_name = db.Column(db.String(250), nullable=True)  # type: ignore
    email = db.Column(db.String(250), unique=True, nullable=False)  # type: ignore
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('users_master', lazy='dynamic'))  # type: ignore

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % self.login

    @property
    def password(self):
        raise AttributeError('Password does not available')

    @password.setter
    def password(self, password: str):
        self._password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self._password_hash, password)

    def get_roles(self) -> list[Role]:
        return [role.name for role in self.roles]

    def has_role(self, role_name: str) -> bool:
        return role_name in self.get_roles()

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'login': self.login,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }


class OAuthUser(db.Model, TimeStampedMixin, UUIDMixin):  # type: ignore
    __tablename__ = "oauth_users"

    user_id = db.Column(UUIDType(binary=False), db.ForeignKey('users_master.id'), nullable=False)  # type: ignore
    user = db.relationship(User, backref=db.backref('oauth_users', lazy=True))  # type: ignore

    oauth_id = db.Column(db.String(255), nullable=False)  # type: ignore
    oauth_name = db.Column(db.String(255), nullable=False)  # type: ignore

    __table_args__ = (db.UniqueConstraint('oauth_id', 'oauth_name', name='uniq_oauth_id_name'), )  # type: ignore

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<OAuth {self.oauth_name}:{self.oauth_id}>"


class UserSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = User
        exclude = ('_password_hash',)
        unknown = EXCLUDE

    @validates('login')
    def validate_login(self, value):
        from app.main import get_current_app

        if get_current_app().user_service.is_login_registered(value):  # type: ignore
            get_logger().debug(f'Валидация модели. Login {value} уже занят.')
            raise ModelSchemaValidationException('Login already exists.')

    @validates('email')
    def validate_email(self, value):
        from app.main import get_current_app

        if get_current_app().user_service.is_email_registered(value):  # type: ignore
            get_logger().debug(f'Валидация модели. Email {value} уже занят.')
            raise ModelSchemaValidationException('Email is already registered.')


class OAuthUserSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = OAuthUser
        unknown = EXCLUDE
