import http
from unittest.mock import ANY

import pytest

from app.models.user import User


@pytest.fixture
def wait_response_login():
    return {
        'access_token': ANY,
        'refresh_token': ANY,
    }


def test_login_ok(client, login_url, login, password,
                  make_body_for_login, clear_model, create_default_user,
                  wait_response_login):

    clear_model(User)
    create_default_user()

    response = client.post(
        path=login_url,
        data=make_body_for_login(login=login, password=password),
    )

    assert response.status_code == http.HTTPStatus.OK

    result = response.json
    assert result == wait_response_login


def test_login_empty_body(client, login_url,
                          clear_model, create_default_user):

    clear_model(User)
    create_default_user()

    response = client.post(
        path=login_url,
        data={}
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_login_blank_password(client, login_url, login,
                              make_body_for_login, clear_model, create_default_user):

    clear_model(User)
    create_default_user()

    response = client.post(
        path=login_url,
        data=make_body_for_login(login=login, password=''),
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_login_after_delete_user(client, login_url, login, password, make_body_for_login,
                                 clear_model, create_default_user):

    clear_model(User)
    create_default_user()

    response = client.post(
        path=login_url,
        data=make_body_for_login(login=login, password=password),
    )

    assert response.status_code == http.HTTPStatus.OK

    clear_model(User)

    response = client.post(
        path=login_url,
        data=make_body_for_login(login=login, password=password),
    )

    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
