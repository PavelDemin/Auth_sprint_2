from app.exceptions import DataBaseException, ModelSchemaValidationException
from app.logging import get_logger
from app.models.user import User, UserSchema
from app.storage.db import db
from flask import Flask
from sqlalchemy.exc import DatabaseError


class UserService:
    model = User
    schema = UserSchema

    def create_user(self, data: dict) -> User:

        self.schema().load(data)

        password = data.pop('password', None)
        if password is None:
            raise DataBaseException('')

        user = self.model(**data)
        user.password = password

        db.session.add(user)

        try:
            db.session.commit()

        except DatabaseError as exception:
            get_logger().error(exception)
            raise DataBaseException('')
        else:
            return user

    def change_password(self, user_id: str, password: str):
        user = self.get_by_id(user_id)
        user.password = password
        db.session.add(user)
        db.session.commit()

    def change_login(self, user_id: str, login: str):

        if self.get_by_login(login):
            get_logger().debug(f'Валидация модели. Login {login} уже занят.')
            raise ModelSchemaValidationException('Login already exists.')

        user = self.get_by_id(user_id)
        user.login = login

        db.session.add(user)
        db.session.commit()

    def get_by_id(self, value):
        return User.query.get_or_404(value)

    def get_by_login(self, value):
        return self.model.query.filter_by(login=value).first()

    def get_by_email(self, value):
        return self.model.query.filter_by(email=value).first()

    def is_login_registered(self, value):
        return bool(self.get_by_login(value))

    def is_email_registered(self, value):
        return bool(self.get_by_email(value))


def init_userservice(app: Flask):
    app.user_service = UserService()  # type: ignore
