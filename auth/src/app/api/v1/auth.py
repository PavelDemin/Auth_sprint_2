from flask import Blueprint
from flask.wrappers import Response
from flask_jwt_extended import jwt_required

from app.services.auth_service import AuthService
from app.utils.limiter import LimiterRequests

from .schemas import (ChangeLoginSchema, ChangePasswordSchema, LoginSchema,
                      PaginationSchema, SignUpSchema)
from .utils.request_validator import RequestValidator

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/test', methods=['GET', ])
@LimiterRequests()
def test_route():
    return 'It works'


@auth_bp.route('/test_jwt', methods=['GET', ])
@LimiterRequests()
@jwt_required()
def test_jwt_route():
    return 'It works'


@auth_bp.route('/login', methods=['POST'])
@LimiterRequests()
@RequestValidator.validate_body(schema=LoginSchema)
def login(data, auth_service: AuthService) -> tuple[Response, int]:
    """Вход пользователя в систему
    ---
    post:
      description: Вход пользователя в аккаунт
      requestBody:
        content:
          application/json:
            schema: LoginSchema
      responses:
        200:
          description: Аутентификация удалась
          content:
            application/json:
              schema: JWTResponseSchema
        400:
          description: Некорректный запрос
        401:
          description: Аутентификация не удалась
        429:
          description: Отправилено слишком много запросов
      tags:
        - Пользователь
    """
    return auth_service.login(data)


@auth_bp.route('/signup', methods=['POST'])
@LimiterRequests()
@RequestValidator.validate_body(schema=SignUpSchema)
def sign_up(data, auth_service: AuthService) -> tuple[Response, int]:
    """Регистрация пользователя в системе
    ---
    post:
      description: Регистрация пользователя
      requestBody:
        content:
          application/json:
            schema: SignUpSchema
      responses:
        201:
          description: Пользователь успешно создан
          content:
            application/json:
              schema: UserResponseSchema
        400:
          description: Некорректный запрос
        409:
          description: Ошибка валидации данных
        429:
          description: Отправилено слишком много запросов
      tags:
        - Пользователь
    """
    return auth_service.signup(data)


@auth_bp.route('/logout', methods=['GET'])
@LimiterRequests()
@jwt_required()
def logout(auth_service: AuthService) -> Response:
    """Выход из аккаунта
    ---
    get:
      description: Запрос на выход из аккаунта на текущем устройстве
      security:
        - jwt_token: []
      responses:
        200:
          description: Успешный выход из аккаунта
        400:
          description: Некорректный запрос
        401:
          description: Необходима авторизация
        429:
          description: Отправилено слишком много запросов
      tags:
        - Пользователь
    """
    return auth_service.logout()


@auth_bp.route('/logout_all', methods=['GET'])
@LimiterRequests()
@jwt_required()
def logout_all(auth_service: AuthService) -> Response:
    """Выход из аккаунта на всех устройствах
    ---
    get:
      description: Запрос на выход из аккаунта со всех устройств
      security:
        - jwt_token: []
      responses:
        200:
          description: Успешный выход из аккаунта на всех устройствах
        400:
          description: Некорректный запрос
        401:
          description: Необходима авторизация
        429:
          description: Отправилено слишком много запросов
      tags:
        - Пользователь
    """
    return auth_service.logout_all()


@auth_bp.route('/refresh', methods=['GET'])
@LimiterRequests()
@jwt_required(refresh=True)
def refresh(auth_service: AuthService) -> Response:
    """Получение новых токенов
    ---
    get:
      description: Получение новых токенов на основе refresh токена
      security:
        - jwt_token: []
      responses:
        200:
          description: Токены успешно получены
          content:
            application/json:
              schema: JWTResponseSchema
        400:
          description: Некорректный запрос
        401:
          description: Необходима авторизация
        429:
          description: Отправилено слишком много запросов
      tags:
        - Пользователь
    """
    return auth_service.refresh_jwt()


@auth_bp.route('/change_password', methods=['POST'])
@LimiterRequests()
@jwt_required(fresh=True)
@RequestValidator.validate_body(schema=ChangePasswordSchema)
def change_password(data, auth_service: AuthService) -> Response:
    """Изменение пароля
    ---
    post:
      description: Изменение пароля учетной записи
      security:
        - jwt_token: []
      requestBody:
        content:
          application/json:
            schema: ChangePasswordSchema
      responses:
        200:
          description: Пароль успешно изменён
        400:
          description: Некорректный запрос
        401:
          description: Необходима авторизация
        429:
          description: Отправилено слишком много запросов
      tags:
        - Пользователь
    """
    return auth_service.change_password(data)


@auth_bp.route('/change_login', methods=['POST'])
@LimiterRequests()
@jwt_required(fresh=True)
@RequestValidator.validate_body(schema=ChangeLoginSchema)
def change_login(data, auth_service: AuthService) -> Response:
    """Изменение логина
    ---
    post:
      description: Изменение логина учетной записи
      security:
        - jwt_token: []
      requestBody:
        content:
          application/json:
            schema: ChangeLoginSchema
      responses:
        200:
          description: Логин успешно изменён
        400:
          description: Некорректный запрос
        401:
          description: Необходима авторизация
        409:
          description: Ошибка валидации данных
        429:
          description: Отправилено слишком много запросов
      tags:
        - Пользователь
    """
    return auth_service.change_login(data)


@auth_bp.route('/history', methods=['GET'])
@LimiterRequests()
@jwt_required()
@RequestValidator.validate_path_args(schema=PaginationSchema)
def auth_history(data, auth_service: AuthService) -> Response:
    """Получение истории входа пользователем
    ---
    get:
      description: Получение истории входа пользователем
      security:
        - jwt_token: []
      parameters:
        - name: page
          in: query
          description: number of page
          required: true
          type: integer
      responses:
        200:
          description: История входа
          content:
            application/json:
              schema: AuthHistorySchema
        401:
          description: Необходима авторизация
        429:
          description: Отправилено слишком много запросов
      tags:
        - Пользователь
    """
    return auth_service.auth_history(page=data['page'])


@auth_bp.route('/is_authorise', methods=['GET'])
@LimiterRequests()
@jwt_required()
def is_authorise(auth_service: AuthService) -> Response:
    """Проверка на авторизацию пользователя
    ---
    get:
      description: Проверка на авторизацию пользователя
      security:
        - jwt_token: []
      responses:
        200:
          description: Пользователь авторизован
        401:
          description: Необходима авторизация
        429:
          description: Отправлено слишком много запросов
      tags:
        - Пользователь
    """
    return auth_service.is_authorise()
