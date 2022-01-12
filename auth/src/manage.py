from gevent import monkey

monkey.patch_all()

from typing import Optional

import typer
from gevent.pywsgi import WSGIServer
from IPython import embed

from app.logging import get_logger
from app.main import app
from app.models.role import DefaultRoleEnum
from app.services.role_service import RoleService
from app.services.user_service import UserService
from app.settings import settings

typer_app = typer.Typer()


@typer_app.command()
def shell():
    embed()


@typer_app.command()
def runserver():

    http_server = WSGIServer(
        (settings.WSGI.HOST, settings.WSGI.PORT), app, spawn=settings.WSGI.workers
    )
    http_server.serve_forever()


@typer_app.command(name='create_admin')
def create_admin(login: Optional[str] = typer.Option(None),
                 password: Optional[str] = typer.Option(None),
                 email: Optional[str] = typer.Option(None)) -> None:

    if not login:
        login = settings.DEFAULT_ADMIN_LOGIN

    if not password:
        password = settings.DEFAULT_ADMIN_PASSWORD

    if not email:
        email = settings.DEFAULT_ADMIN_EMAIL

    user_data = {
        'login': login,
        'password': password,
        'email': email,
    }

    user_service = UserService()
    role_service = RoleService()

    try:
        user = user_service.create_user(user_data)
        role = role_service.get_by_name(DefaultRoleEnum.admin.value)
        role_service.assign_role(data={'user_id': user.id, 'role_id': role.id})
        typer.echo(user.id)
    except Exception as exception:
        get_logger().error(exception)
        raise ValueError(exception)

if __name__ == '__main__':
    typer_app()
