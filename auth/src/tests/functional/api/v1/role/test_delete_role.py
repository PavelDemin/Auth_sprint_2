from http import HTTPStatus

from app.models.role import Role
from app.models.user import User
from manage import typer_app
from typer.testing import CliRunner

runner = CliRunner()


def test_delete_role_by_user_without_admin_role(client, clear_model, create_default_user, delete_role_url,
                                                login_default_user, make_access_header, fake_role_id):
    clear_model(User)
    clear_model(Role)

    create_default_user()
    tokens = login_default_user()
    headers = make_access_header(tokens)
    response = client.delete(
        path=delete_role_url,
        headers=headers,
        json={
            'id': fake_role_id
        })
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_role_by_admin(client, clear_model, delete_role_url, login_default_user, make_access_header,
                              create_role_url):
    clear_model(User)
    clear_model(Role)

    runner.invoke(typer_app, ['create_admin'])
    tokens = login_default_user(login='admin', password='admin')
    headers = make_access_header(tokens)
    response_role = client.post(
        path=create_role_url,
        headers=headers,
        json={
            'description': 'string',
            'name': ''
        })
    resp = response_role.json
    response = client.delete(
        path=delete_role_url,
        headers=headers,
        json={
            'id': resp['id']
        })
    assert response.status_code == HTTPStatus.OK
    assert response.json == {}


def test_delete_fake_role_by_admin(client, clear_model, delete_role_url, login_default_user, make_access_header,
                                   fake_role_id):
    clear_model(User)
    clear_model(Role)

    runner.invoke(typer_app, ['create_admin'])
    tokens = login_default_user(login='admin', password='admin')
    headers = make_access_header(tokens)
    response = client.delete(
        path=delete_role_url,
        headers=headers,
        json={
            'id': fake_role_id
        })
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_role_with_empty_body(client, clear_model, delete_role_url, login_default_user, make_access_header):

    clear_model(User)
    clear_model(Role)

    runner.invoke(typer_app, ['create_admin'])
    tokens = login_default_user(login='admin', password='admin')
    headers = make_access_header(tokens)
    response = client.delete(
        path=delete_role_url,
        headers=headers,
        json={})
    assert response.status_code == HTTPStatus.BAD_REQUEST
