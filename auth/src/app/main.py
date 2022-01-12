from flask import Flask
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

from app.api import v1 as api_v1
from app.dependencies import configure
from app.exceptions import init_error_handler
from app.logging import init_log_config
from app.openapi.swagger import init_swagger
from app.services.role_service import init_roleservice
from app.services.user_service import UserService, init_userservice
from app.settings import settings
from app.storage.db import init_db
from app.utils.limiter import init_limiter

app = Flask(settings.FLASK_APP)
ma = Marshmallow()
jwt = JWTManager()

app.config['DEBUG'] = settings.DEBUG
app.config['SECRET_KEY'] = settings.SECRET_KEY

init_db(app)
init_userservice(app)
init_roleservice(app)
init_limiter(app)

ma.init_app(app)
api_v1.create_api(app)
jwt.init_app(app)


@jwt.user_identity_loader
def user_identity_loader(user) -> str:
    return str(user.id)


@jwt.user_lookup_loader
def user_lookup_loader(jwt_header: dict, jwt_payload: dict):
    return UserService().get_by_id(jwt_payload['sub'])


init_swagger(app)
init_error_handler(app)

FlaskInjector(app=app, modules=[configure])

app.app_context().push()


def get_current_app() -> Flask:
    return app
