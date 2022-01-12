from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from app.settings import settings


def init_swagger(app: Flask):

    swagger_url = settings.SWAGGER.URL
    swagger_json_url = settings.SWAGGER.JSON_URL

    swagger_bp = get_swaggerui_blueprint(
        swagger_url,
        swagger_json_url,
        config={'app_name': 'Auth app'},
    )

    app.register_blueprint(swagger_bp)

    @app.route('/openapi/swagger.json')
    def get_openapi_spec():
        spec = APISpec(
            title='Auth - сервис аутентификации и авторизации',
            version='0.1.0',
            openapi_version='3.0.3',
            info=dict(
                description='Сервис регистрации пользователя, входа пользователя в аккаунт, '
                            'обновление access-токена, выход пользователя из аккаунта, изменение логина и пароля.'
            ),
            plugins=[FlaskPlugin(), MarshmallowPlugin()],
        )

        jwt_token = {'type': 'http', 'scheme': 'bearer', 'bearerFormat': 'JWT'}
        spec.components.security_scheme('jwt_token', jwt_token)

        with app.test_request_context():
            for rule in app.url_map.iter_rules():
                spec.path(view=app.view_functions[rule.endpoint])

        return jsonify(spec.to_dict())
