from flask import Blueprint, Flask

from .auth import auth_bp
from .oauth import oauth_bp
from .role import role_bp


def create_api(app: Flask) -> None:

    api = Blueprint('api', __name__, url_prefix='/api/v1/')

    api.register_blueprint(oauth_bp)
    api.register_blueprint(auth_bp)
    api.register_blueprint(role_bp)

    app.register_blueprint(api)
