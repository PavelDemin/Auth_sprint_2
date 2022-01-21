from app.services.oauth_service import OAuthService
from app.utils.limiter import LimiterRequests
from flask import Blueprint, jsonify, redirect, request, url_for
from flask.wrappers import Response

from .schemas import OAuthPathParameterSchema
from .utils.request_validator import RequestValidator

oauth_bp = Blueprint('oauth', __name__, url_prefix='/oauth')


@oauth_bp.route('/test', methods=['GET', ])
@LimiterRequests()
def test_route():
    return 'It works'


@oauth_bp.route('/login/<string:service>', methods=['GET'])
@LimiterRequests()
@RequestValidator.validate_path_parameters(schema=OAuthPathParameterSchema)
def login(service, oauth_service: OAuthService):
    """Запрос на доступ к аккаунту сервиса с помощью OAuth
    ---
    get:
      description: Запрос на доступ к аккаунту сервиса с помощью OAuth
      parameters: [
          {
            in: path,
            name: service,
            required: true,
            type: string,
            enum: [yandex, google]
          }
        ]
      responses:
        301:
          description: Переход на страницу авторизации сервиса OAuth
        400:
          description: Некорректный запрос
        429:
          description: Отправилено слишком много запросов
      tags:
        - OAuth
    """

    redirect_url = url_for('api.oauth.auth', service=service, _external=True)
    return oauth_service.authorize_redirect(redirect_url=redirect_url, service=service)


@oauth_bp.route('/auth/<string:service>', methods=['GET'])
@LimiterRequests()
@RequestValidator.validate_path_parameters(schema=OAuthPathParameterSchema)
def auth(service, oauth_service: OAuthService) -> Response:
    """Аутификация с помощью OAuth
    ---
    get:
      description: Аутентификация с помощью OAuth
      parameters: [
          {
            in: path,
            name: service,
            required: true,
            type: string,
            enum: [yandex, google]
          }
        ]
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
        - OAuth
    """

    return oauth_service.auth(service=service)
