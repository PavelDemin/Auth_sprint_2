from app.models.role import Role
from app.models.user import User
from manage import typer_app as app
from typer.testing import CliRunner

runner = CliRunner()


def test_create_admin(clear_model):

    clear_model(User)
    clear_model(Role)

    result = runner.invoke(app, ['create_admin'])

    assert result.exit_code == 0
