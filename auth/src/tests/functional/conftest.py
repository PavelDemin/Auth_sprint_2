from urllib.parse import urljoin

import pytest
from app.main import app
from app.models.role import DefaultRoleEnum, Role
from app.services.role_service import RoleService
from app.storage.db import db


@pytest.fixture
def auth_url():
    return '/api/v1/auth/'


@pytest.fixture
def role_url():
    return '/api/v1/roles/'


@pytest.fixture
def oauth_url():
    return '/api/v1/oauth/'


@pytest.fixture
def login_url(auth_url):
    return urljoin(auth_url, 'login')


@pytest.fixture
def signup_url(auth_url):
    return urljoin(auth_url, 'signup')


@pytest.fixture
def login():
    return 'signup'


@pytest.fixture
def password():
    return 'signup'


@pytest.fixture
def email():
    return 'signup_o@test.ru'


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def clear_model():
    def inner(model):
        db.session.query(model).delete()
        db.session.commit()

        if model is Role:
            create_default_roles()

    return inner


def create_default_roles():
    role_service = RoleService()
    for default_role in DefaultRoleEnum:
        role_service.create_role({'name': default_role.value, 'description': ''})


@pytest.fixture
def create_default_user(client, signup_url, login, password, email, make_body_for_signup):

    def inner():
        response = client.post(
            path=signup_url,
            data=make_body_for_signup(login=login, password=password, email=email),
        )
        return response.json
    return inner


@pytest.fixture
def login_default_user(login_user, login, password):

    def inner(login=login, password=password):
        response = login_user(login=login, password=password)
        return response.json

    return inner


@pytest.fixture
def login_user(client, login_url, make_body_for_login):

    def inner(login, password):
        response = client.post(
            path=login_url,
            data=make_body_for_login(login=login, password=password),
        )
        return response
    return inner


@pytest.fixture
def make_access_header():

    def inner(tokens):
        access_token = tokens['access_token']
        return {'Authorization': f'Bearer {access_token}'}
    return inner


@pytest.fixture
def make_refresh_header():

    def inner(tokens):
        refresh_token = tokens['refresh_token']
        return {'Authorization': f'Bearer {refresh_token}'}
    return inner


@pytest.fixture
def make_body_for_signup():
    def inner(login, password, email):
        return {
            'login': login,
            'password': password,
            'first_name': '',
            'last_name': '',
            'email': email,
        }
    return inner


@pytest.fixture
def make_body_for_login():
    def inner(login, password):
        return {
            'login': login,
            'password': password,
        }
    return inner
