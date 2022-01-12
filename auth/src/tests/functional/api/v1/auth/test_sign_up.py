import http
from unittest.mock import ANY

import pytest

from app.models.user import User


@pytest.fixture
def wait_response_sign_up():
    def inner(login, email):
        return {
            'id': ANY,
            'login': login,
            'first_name': '',
            'last_name': '',
            'email': email,
        }
    return inner


def test_signup_ok(client, signup_url, login, password, email,
                   wait_response_sign_up, make_body_for_signup, clear_model):

    clear_model(User)

    response = client.post(
        path=signup_url,
        data=make_body_for_signup(login=login, password=password, email=email),
    )

    assert response.status_code == http.HTTPStatus.CREATED

    result = response.json
    assert result == wait_response_sign_up(login=login, email=email)


def test_signup_login_exist(client, signup_url, login, password, email, make_body_for_signup, clear_model):

    clear_model(User)

    response = client.post(
        path=signup_url,
        data=make_body_for_signup(login=login, password=password, email=email),
    )

    assert response.status_code == http.HTTPStatus.CREATED

    new_email = 'new_' + email

    response = client.post(
        path=signup_url,
        data=make_body_for_signup(login=login, password=password, email=new_email),
    )

    assert response.status_code == http.HTTPStatus.CONFLICT


def test_signup_email_exist(client, signup_url, login, password, email, make_body_for_signup, clear_model):

    clear_model(User)

    response = client.post(
        path=signup_url,
        data=make_body_for_signup(login=login, password=password, email=email),
    )

    assert response.status_code == http.HTTPStatus.CREATED

    new_login = 'new_' + login

    response = client.post(
        path=signup_url,
        data=make_body_for_signup(login=new_login, password=password, email=email),
    )

    assert response.status_code == http.HTTPStatus.CONFLICT

def test_signup_empty_body(client, signup_url, login, email, make_body_for_signup, clear_model):

    clear_model(User)

    response = client.post(
        path=signup_url,
        data={},
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST

def test_signup_blank_login(client, signup_url, password, email, make_body_for_signup, clear_model):

    clear_model(User)

    response = client.post(
        path=signup_url,
        data=make_body_for_signup(login='', password=password, email=email),
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST

def test_signup_blank_email(client, signup_url, password, login, make_body_for_signup, clear_model):

    clear_model(User)

    response = client.post(
        path=signup_url,
        data=make_body_for_signup(login=login, password=password, email=''),
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST

def test_signup_blank_password(client, signup_url, login, email, make_body_for_signup, clear_model):

    clear_model(User)

    response = client.post(
        path=signup_url,
        data=make_body_for_signup(login=login, password='', email=email),
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST

def test_signup_bad_email(client, signup_url, login, password, make_body_for_signup, clear_model):

    clear_model(User)

    response = client.post(
        path=signup_url,
        data=make_body_for_signup(login=login, password=password, email='email'),
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST

    response = client.post(
        path=signup_url,
        data=make_body_for_signup(login=login, password=password, email='email@'),
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST

    response = client.post(
        path=signup_url,
        data=make_body_for_signup(login=login, password=password, email='email@email'),
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST

    response = client.post(
        path=signup_url,
        data=make_body_for_signup(login=login, password=password, email='email@email.'),
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST
