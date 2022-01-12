from http import HTTPStatus

from app.models.role import Role
from app.models.user import User
from manage import typer_app
from typer.testing import CliRunner

runner = CliRunner()


def test_unassign_role_by_user_without_admin_role(client, clear_model, create_default_user, create_role_url,
                                                  assign_role_url, unassign_role_url, login_default_user,
                                                  make_access_header, fake_role_id):
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
            'name': 'New Role'
        })
    resp = response_role.json
    default_user = create_default_user()
    tokens = login_default_user()
    headers = make_access_header(tokens)
    client.post(
        path=assign_role_url,
        headers=headers,
        json={
            'role_id': resp['id'],
            'user_id': default_user['id']
        })
    response = client.delete(
        path=unassign_role_url,
        headers=headers,
        json={
            'role_id': resp['id'],
            'user_id': default_user['id']
        })
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_unassign_role_by_admin(client, clear_model, assign_role_url, login_default_user, make_access_header,
                                create_role_url, create_default_user, unassign_role_url):
    clear_model(User)
    clear_model(Role)

    default_user = create_default_user()
    runner.invoke(typer_app, ['create_admin'])
    tokens = login_default_user(login='admin', password='admin')
    headers = make_access_header(tokens)
    response_role = client.post(
        path=create_role_url,
        headers=headers,
        json={
            'description': 'string',
            'name': 'New Role'
        })
    resp = response_role.json
    client.post(
        path=assign_role_url,
        headers=headers,
        json={
            'role_id': resp['id'],
            'user_id': default_user['id']
        })
    response = client.delete(
        path=unassign_role_url,
        headers=headers,
        json={
            'role_id': resp['id'],
            'user_id': default_user['id']
        })
    assert response.status_code == HTTPStatus.OK


def test_unassign_role_with_empty_body(client, clear_model, unassign_role_url, login_default_user, make_access_header):

    clear_model(User)
    clear_model(Role)

    runner.invoke(typer_app, ['create_admin'])
    tokens = login_default_user(login='admin', password='admin')
    headers = make_access_header(tokens)
    response = client.delete(
        path=unassign_role_url,
        headers=headers,
        json={})
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_unassign_role_with_fake_role_id(client, clear_model, assign_role_url, login_default_user, make_access_header,
                                         create_default_user, create_role_url, unassign_role_url, fake_role_id):
    clear_model(User)
    clear_model(Role)

    default_user = create_default_user()
    runner.invoke(typer_app, ['create_admin'])
    tokens = login_default_user(login='admin', password='admin')
    headers = make_access_header(tokens)
    response_role = client.post(
        path=create_role_url,
        headers=headers,
        json={
            'description': 'string',
            'name': 'New Role'
        })
    resp = response_role.json
    client.post(
        path=assign_role_url,
        headers=headers,
        json={
            'role_id': resp['id'],
            'user_id': default_user['id']
        })
    response = client.delete(
        path=unassign_role_url,
        headers=headers,
        json={
            'role_id': fake_role_id,
            'user_id': default_user['id']
        })
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_assign_role_with_fake_user_id(client, clear_model, assign_role_url, login_default_user, make_access_header,
                                       create_role_url, create_default_user, unassign_role_url, fake_user_id):
    clear_model(User)
    clear_model(Role)

    default_user = create_default_user()
    runner.invoke(typer_app, ['create_admin'])
    tokens = login_default_user(login='admin', password='admin')
    headers = make_access_header(tokens)
    response_role = client.post(
        path=create_role_url,
        headers=headers,
        json={
            'description': 'string',
            'name': 'New Role'
        })
    resp = response_role.json
    client.post(
        path=assign_role_url,
        headers=headers,
        json={
            'role_id': resp['id'],
            'user_id': default_user['id']
        })
    response = client.delete(
        path=unassign_role_url,
        headers=headers,
        json={
            'role_id': resp['id'],
            'user_id': fake_user_id
        })
    assert response.status_code == HTTPStatus.NOT_FOUND
