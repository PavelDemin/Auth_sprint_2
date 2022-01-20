from http import HTTPStatus

from typer.testing import CliRunner

from app.models.role import Role
from app.models.user import User
from manage import typer_app

runner = CliRunner()


def test_update_role_by_user_without_admin_role(client, clear_model, create_default_user, update_role_url,
                                                login_default_user, make_access_header, fake_role_id):
    clear_model(User)
    clear_model(Role)

    create_default_user()
    tokens = login_default_user()
    headers = make_access_header(tokens)
    response = client.put(
        path=update_role_url,
        headers=headers,
        json={
            'description': 'New string',
            'id': fake_role_id,
            'name': 'New string'
        })
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_role_by_admin(client, clear_model, update_role_url, login_default_user, make_access_header,
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
    response = client.put(
        path=update_role_url,
        headers=headers,
        json={
            'description': 'New string',
            'id': resp['id'],
            'name': 'New string'
        })
    assert response.status_code == HTTPStatus.OK


def test_update_fake_role_by_admin(client, clear_model, update_role_url, login_default_user, make_access_header,
                                   fake_role_id):
    clear_model(User)
    clear_model(Role)

    runner.invoke(typer_app, ['create_admin'])
    tokens = login_default_user(login='admin', password='admin')
    headers = make_access_header(tokens)
    response = client.put(
        path=update_role_url,
        headers=headers,
        json={
            'description': 'New string',
            'id': fake_role_id,
            'name': 'New string'
        })
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_role_with_empty_body(client, clear_model, update_role_url, login_default_user, make_access_header):

    clear_model(User)
    clear_model(Role)

    runner.invoke(typer_app, ['create_admin'])
    tokens = login_default_user(login='admin', password='admin')
    headers = make_access_header(tokens)
    response = client.put(
        path=update_role_url,
        headers=headers,
        json={})
    assert response.status_code == HTTPStatus.BAD_REQUEST
