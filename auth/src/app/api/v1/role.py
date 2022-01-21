from app.services.role_service import RoleService
from app.utils.limiter import LimiterRequests
from flask import Blueprint
from flask.wrappers import Response
from flask_jwt_extended import jwt_required

from .schemas import (AssignRoleSchema, DeleteRoleSchema, ResponseRoleSchema,
                      RolesSchema, UnassignRoleSchema)
from .utils.access_decorator import admin_required
from .utils.request_validator import RequestValidator

role_bp = Blueprint('roles', __name__, url_prefix='/roles')


@role_bp.route('/create_role', methods=['POST'])
@LimiterRequests()
@jwt_required()
@admin_required
@RequestValidator.validate_body(schema=RolesSchema)
def create_role(data, role_service: RoleService) -> tuple[Response, int]:
    """Создание роли в системе
        ---
        post:
          description: Создание роли в системе
          security:
            - jwt_token: []
          requestBody:
            content:
              application/json:
                schema: RolesSchema
          responses:
            200:
              description: Роль успешно создана
              content:
                application/json:
                  schema: ResponseRoleSchema
            400:
              description: Некорректный запрос
            401:
              description: Необходима авторизация
            403:
              description: Недостаточно прав для выполнения данного запроса
            429:
              description: Отправилено слишком много запросов
          tags:
            - Роль
        """
    return role_service.create_role(data)


@role_bp.route('/delete_role', methods=['DELETE'])
@LimiterRequests()
@jwt_required()
@admin_required
@RequestValidator.validate_body(schema=DeleteRoleSchema)
def delete_role(data, role_service: RoleService) -> tuple[Response, int]:
    """Удалить роль из системы
        ---
        delete:
          description: Удалить роль из системы
          security:
            - jwt_token: []
          requestBody:
            content:
              application/json:
                schema: DeleteRoleSchema
          responses:
            200:
              description: Роль успешно удалена
            400:
              description: Некорректный запрос
            401:
              description: Необходима авторизация
            403:
              description: Недостаточно прав для выполнения данного запроса
            404:
              description: Роль не найдена
            429:
              description: Отправилено слишком много запросов
          tags:
            - Роль
        """
    return role_service.delete_role(data)


@role_bp.route('/update_role', methods=['PUT'])
@LimiterRequests()
@jwt_required()
@admin_required
@RequestValidator.validate_body(schema=ResponseRoleSchema)
def update_role(data, role_service: RoleService) -> tuple[Response, int]:
    """Обновить данные роли
        ---
        put:
          description: Обновить роль
          security:
            - jwt_token: []
          requestBody:
            content:
              application/json:
                schema: ResponseRoleSchema
          responses:
            200:
              description: Роль успешно обновлена
            400:
              description: Некорректный запрос
            401:
              description: Необходима авторизация
            403:
              description: Недостаточно прав для выполнения данного запроса
            404:
              description: Роль не найдена
            429:
              description: Отправилено слишком много запросов
          tags:
            - Роль
        """
    return role_service.update_role(data)


@role_bp.route('/get_role/<uuid:role_id>', methods=['GET'])
@LimiterRequests()
@jwt_required()
@admin_required
def get_role(role_id, role_service: RoleService) -> tuple[Response, int]:
    """Получить данные роли
        ---
        get:
          description: Получить роль
          security:
            - jwt_token: []
          parameters:
            - in: path
              name: role_id
              schema:
                type: string
                format: uuid
              required: true
              description: UUID ID of the role to get
          responses:
            200:
              description: Роль успешно Получена
              content:
                application/json:
                  schema: ResponseRoleSchema
            400:
              description: Некорректный запрос
            401:
              description: Необходима авторизация
            403:
              description: Недостаточно прав для выполнения данного запроса
            404:
              description: Роль не найдена
            429:
              description: Отправилено слишком много запросов
          tags:
            - Роль
        """
    return role_service.get_role(role_id)


@role_bp.route('/get_roles', methods=['GET'])
@LimiterRequests()
@jwt_required()
@admin_required
def get_roles(role_service: RoleService) -> tuple[Response, int]:
    """Получить все роли
        ---
        get:
          description: Получить роли
          security:
            - jwt_token: []
          responses:
            200:
              description: Роли успешно получены
              content:
                application/json:
                  schema:
                    type: array
                    items: ResponseRoleSchema
            400:
              description: Некорректный запрос
            401:
              description: Необходима авторизация
            404:
              description: Роли не найдены
            429:
              description: Отправилено слишком много запросов
          tags:
            - Роль
        """
    return role_service.get_roles()


@role_bp.route('/assign_role', methods=['POST'])
@LimiterRequests()
@jwt_required()
@admin_required
@RequestValidator.validate_body(schema=AssignRoleSchema)
def assign_role(data, role_service: RoleService) -> tuple[Response, int]:
    """Добавление роли пользователю
        ---
      post:
        description: Добавить роль пользователю
        security:
        - jwt_token: []
        requestBody:
          content:
            application/json:
              schema: AssignRoleSchema
        responses:
          200:
            description: Роль успешно добавлена
          400:
            description: Некорректный запрос
          401:
            description: Необходима авторизация
          403:
            description: Недостаточно прав для выполнения данного запроса
          404:
            description: Роли или пользователь не найдены
          429:
            description: Отправилено слишком много запросов
        tags:
          - Роль
        """
    return role_service.assign_role(data=data)


@role_bp.route('/unassign_role', methods=['DELETE'])
@LimiterRequests()
@jwt_required()
@admin_required
@RequestValidator.validate_body(schema=UnassignRoleSchema)
def unassign_role(data, role_service: RoleService) -> tuple[Response, int]:
    """Удаление роли у пользователя
        ---
        delete:
          description: Удалить роль пользователю
          security:
          - jwt_token: []
          requestBody:
            content:
              application/json:
                schema: UnassignRoleSchema
          responses:
            200:
              description: Роль успешно удалена
            400:
              description: Некорректный запрос
            401:
              description: Необходима авторизация
            403:
              description: Недостаточно прав для выполнения данного запроса
            404:
              description: Роли или пользователь не найдены
            429:
              description: Отправилено слишком много запросов
          tags:
            - Роль
        """
    return role_service.unassign_role(data=data)
