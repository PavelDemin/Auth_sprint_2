from http import HTTPStatus

from app.exceptions import (DataBaseException, InvalidRefreshTokenException,
                            WrongCredentialsException)
from app.logging import get_logger
from app.models.auth_history import AuthHistory
from app.services.jwt_service import JWTService
from app.services.user_service import UserService
from app.settings import settings
from flask import jsonify
from flask.wrappers import Response
from injector import inject
from sqlalchemy.exc import SQLAlchemyError


class AuthService:

    @inject
    def __init__(self, user_service: UserService, token_service: JWTService):
        self.user_service = user_service
        self.token_service = token_service

    def signup(self, data: dict) -> tuple[Response, int]:
        user = self.user_service.create_user(data)
        return jsonify(user.to_dict()), HTTPStatus.CREATED

    def login(self, data: dict) -> tuple[Response, int]:
        login = data['login']
        user = self.user_service.get_by_login(login)
        if not user or not user.verify_password(data['password']):
            get_logger().debug(f'Попытка входа с некорректными данными {login}')
            raise WrongCredentialsException('Failed to enter the account with the current username and password')

        access_token, refresh_token = self.token_service.gen_tokens(user, True)
        self.token_service.save_refresh_token(token=refresh_token, user_id=user.id)

        AuthHistory.add_auth_history(user)

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }), HTTPStatus.OK

    def logout(self) -> Response:
        refresh_jti = self.token_service.get_claim_from_token('refresh_token')
        user_id = self.token_service.get_claim_from_token('sub')

        if not self.token_service.is_exists_refresh_token(refresh_jti, user_id):
            get_logger().debug(f'Попытка выйти из аккаунта по неизвестному токену, юзер {user_id}')
            raise InvalidRefreshTokenException('')

        self.token_service.remove_refresh_token(jti=refresh_jti, user_id=user_id)
        return jsonify()

    def logout_all(self) -> Response:
        refresh_jti = self.token_service.get_claim_from_token('refresh_token')
        user_id = self.token_service.get_claim_from_token('sub')

        if not self.token_service.is_exists_refresh_token(refresh_jti, user_id):
            get_logger().debug(f'Попытка выйти из аккаунта по неизвестному токену, юзер {user_id}')
            raise InvalidRefreshTokenException('')

        self.token_service.remove_refresh_tokens(user_id=user_id)
        return jsonify()

    def refresh_jwt(self) -> Response:
        jti = self.token_service.get_claim_from_token('jti')
        user_id = self.token_service.get_claim_from_token('sub')

        if not self.token_service.is_exists_refresh_token(jti, user_id):
            get_logger().debug(f'Попытка получить токен по неизвестному refresh токену, юзер {user_id}')
            raise InvalidRefreshTokenException('')

        self.token_service.remove_refresh_token(jti=jti, user_id=user_id)
        user = self.user_service.get_by_id(user_id)
        access_token, refresh_token = self.token_service.gen_tokens(user)
        self.token_service.save_refresh_token(token=refresh_token, user_id=user.id)

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        })

    def change_password(self, data) -> Response:
        jti = self.token_service.get_claim_from_token('refresh_token')
        user_id = self.token_service.get_claim_from_token('sub')

        if not self.token_service.is_exists_refresh_token(jti, user_id):
            get_logger().debug(f'Попытка изменить пароль по неизвестному токену, юзер {user_id}')
            raise InvalidRefreshTokenException('')

        self.user_service.change_password(user_id=user_id, password=data['password'])

        return jsonify()

    def change_login(self, data) -> Response:
        jti = self.token_service.get_claim_from_token('refresh_token')
        user_id = self.token_service.get_claim_from_token('sub')

        if not self.token_service.is_exists_refresh_token(jti, user_id):
            get_logger().debug(f'Попытка изменить логин по неизвестному токену, юзер {user_id}')
            raise InvalidRefreshTokenException('')

        self.user_service.change_login(user_id=user_id, login=data['login'])

        return jsonify()

    def auth_history(self, page) -> Response:
        user_id = self.token_service.get_claim_from_token('sub')

        try:
            query = AuthHistory.query.filter_by(user_id=user_id).order_by(
                AuthHistory.timestamp.asc()
            )
            paginator = query.paginate(
                page=page, per_page=settings.PAGINATION_PAGE_LIMIT, error_out=False
            )
        except SQLAlchemyError as exception:
            get_logger().error(f'Ошибка получении истории аутентификации. {str(exception)}')
            raise DataBaseException('')
        else:
            return jsonify([record.to_dict() for record in paginator.items])

    def is_authorise(self) -> Response:
        jti = self.token_service.get_claim_from_token('refresh_token')
        user_id = self.token_service.get_claim_from_token('sub')
        if not self.token_service.is_exists_refresh_token(jti, user_id):
            get_logger().debug(f'Попытка получить статус авторизации по неизвестному токену, юзер {user_id}')
            raise InvalidRefreshTokenException('')
        return jsonify()
