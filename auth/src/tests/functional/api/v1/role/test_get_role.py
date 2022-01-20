from http import HTTPStatus
from unittest.mock import ANY

import pytest
from typer.testing import CliRunner

from app.models.role import Role
from app.models.user import User
from manage import typer_app

runner = CliRunner()


@pytest.fixture
def wait_response_get_roles():
    return [
        {
            'description': ANY,
            'id': ANY,
            'name': ANY
        },
        {
            'description': ANY,
            'id': ANY,
            'name': ANY
        },
        {
            'description': ANY,
            'id': ANY,
            'name': ANY
        }
    ]


def test_get_roles_by_user_without_admin_role(client, clear_model, create_default_user, login_default_user,
                                              make_access_header, get_roles_url):
    clear_model(User)
    clear_model(Role)

    create_default_user()
    tokens = login_default_user()
    headers = make_access_header(tokens)
    response = client.get(
        path=get_roles_url,
        headers=headers)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_get_roles_by_admin(client, clear_model, get_roles_url, login_default_user, make_access_header,
                            wait_response_get_roles):
    clear_model(User)
    clear_model(Role)

    runner.invoke(typer_app, ['create_admin'])
    tokens = login_default_user(login='admin', password='admin')
    headers = make_access_header(tokens)
    response = client.get(
        path=get_roles_url,
        headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json == wait_response_get_roles


def test_get_role_by_admin(client, clear_model, get_roles_url, get_role_url, login_default_user, make_access_header,
                           wait_response_get_role):
    clear_model(User)
    clear_model(Role)

    runner.invoke(typer_app, ['create_admin'])
    tokens = login_default_user(login='admin', password='admin')
    headers = make_access_header(tokens)
    response_roles = client.get(
        path=get_roles_url,
        headers=headers)
    for item in response_roles.json:
        response_role = client.get(
            path=get_role_url + '/' + item['id'],
            headers=headers)
        assert response_role.status_code == HTTPStatus.OK
        assert response_role.json == wait_response_get_role


def test_fake_get_role_by_admin(client, clear_model, get_role_url, login_default_user, make_access_header,
                                fake_role_id):
    clear_model(User)
    clear_model(Role)

    runner.invoke(typer_app, ['create_admin'])
    tokens = login_default_user(login='admin', password='admin')
    headers = make_access_header(tokens)
    response = client.get(
        path=get_role_url,
        headers=headers,
        json={'id': fake_role_id})
    assert response.status_code == HTTPStatus.NOT_FOUND
