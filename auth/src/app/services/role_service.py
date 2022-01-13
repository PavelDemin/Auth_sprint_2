from http import HTTPStatus

from app.exceptions import DataBaseException
from app.logging import get_logger
from app.models.role import Role, RoleSchema
from app.services.user_service import UserService
from app.storage.db import db
from flask import Flask, jsonify
from flask.wrappers import Response
from injector import inject
from sqlalchemy.exc import DatabaseError


class RoleService:
    model = Role
    schema = RoleSchema

    user_service = UserService()

    def create_role(self, data: dict) -> tuple[Response, int]:
        """
        Метод добавляет роль в систему
        :return:
        """
        self.schema().load(data)
        role = self.model(**data)
        db.session.add(role)

        try:
            db.session.commit()

        except DatabaseError as exception:
            get_logger().error(exception)
            raise DataBaseException('')
        else:
            return jsonify(role.to_dict()), HTTPStatus.OK

    def delete_role(self, data: dict) -> tuple[Response, int]:
        """
        Метод удаляет роль из системы
        :return:
        """
        role = self.get_by_id(data['id'])
        if role.name in Role.Meta.PROTECTED_ROLE_NAMES:
            return jsonify('Rejected. This is protected role'), HTTPStatus.BAD_REQUEST

        try:
            db.session.delete(role)
            db.session.commit()

        except DatabaseError as exception:
            get_logger().error(exception)
            raise DataBaseException('')
        else:
            return jsonify(), HTTPStatus.OK

    def update_role(self, data: dict) -> tuple[Response, int]:
        """
        Метод изменяет роль
        :param data:
        :return:
        """
        role = self.get_by_id(data['id'])
        if role.name in Role.Meta.PROTECTED_ROLE_NAMES:
            return jsonify('Rejected. This is protected role'), HTTPStatus.BAD_REQUEST

        role.description = data['description']
        role.name = data['name']
        try:
            db.session.commit()

        except DatabaseError as exception:
            get_logger().error(exception)
            raise DataBaseException('')
        else:
            return jsonify(role.to_dict()), HTTPStatus.OK

    def get_role(self, role_id: str) -> tuple[Response, int]:
        """
        Метод получает роль
        :param role_id:
        :return:
        """
        role = self.get_by_id(role_id)
        if role is None:
            return jsonify(), HTTPStatus.NOT_FOUND
        return jsonify(role.to_dict()), HTTPStatus.OK

    def get_roles(self) -> tuple[Response, int]:
        """
        Метод получает все роли в системе
        :return:
        """
        roles = self.model.query.all()
        if roles is None:
            return jsonify(), HTTPStatus.NOT_FOUND
        prepare_roles = [role.to_dict() for role in roles]
        return jsonify(prepare_roles), HTTPStatus.OK

    def assign_role(self, data):

        user_id = data['user_id']
        role_id = data['role_id']

        user = self.user_service.get_by_id(user_id)
        role = self.get_by_id(role_id)
        user.roles.append(role)
        db.session.add(user)
        try:
            db.session.commit()
        except DatabaseError as exception:
            get_logger().error(exception)
            raise DataBaseException('Exception occured while saving data')
        else:
            return jsonify({}), HTTPStatus.OK

    def unassign_role(self, data):

        user_id = data['user_id']
        role_id = data['role_id']

        user = self.user_service.get_by_id(user_id)
        role = self.get_by_id(role_id)
        if role not in user.roles:
            get_logger().error('Попытка удалить несуществующую роль у пользователя')
            raise DataBaseException('The curent role not exists for the user')
        user.roles.remove(role)

        db.session.add(user)
        try:
            db.session.commit()
        except DatabaseError as exception:
            get_logger().error(exception)
            raise DataBaseException('Exception occured while saving data')
        else:
            return jsonify({}), HTTPStatus.OK

    def get_by_id(self, value) -> Role:
        return Role.query.get_or_404(value)

    def get_by_name(self, value) -> Role:
        return self.model.query.filter_by(name=value).first()


def init_roleservice(app: Flask):
    role_service = RoleService()
    app.role_service = role_service  # type: ignore
