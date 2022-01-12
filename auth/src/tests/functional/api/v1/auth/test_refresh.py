import http
from unittest.mock import ANY

import pytest

from app.models.user import User


@pytest.fixture
def wait_refresh_body():
    return {
        'access_token': ANY,
        'refresh_token': ANY,
    }


def test_refresh(client, refresh_url, make_refresh_header, wait_refresh_body,
                 clear_model, create_default_user, login_default_user):

    clear_model(User)
    create_default_user()
    tokens = login_default_user()
    headers = make_refresh_header(tokens)

    response = client.get(
        path=refresh_url,
        headers=headers,
    )

    assert response.status_code == http.HTTPStatus.OK

    result = response.json
    assert result == wait_refresh_body


def test_refresh_new_token(client, refresh_url, make_refresh_header, wait_refresh_body,
                           clear_model, create_default_user, login_default_user):

    clear_model(User)
    create_default_user()
    tokens = login_default_user()
    headers = make_refresh_header(tokens)

    response = client.get(
        path=refresh_url,
        headers=headers,
    )

    assert response.status_code == http.HTTPStatus.OK

    new_tokens = response.json
    new_headers = make_refresh_header(new_tokens)

    response = client.get(
        path=refresh_url,
        headers=new_headers,
    )

    assert response.status_code == http.HTTPStatus.OK

    result = response.json
    assert result == wait_refresh_body


def test_refresh_old_token(client, refresh_url, make_refresh_header, wait_refresh_body,
                           clear_model, create_default_user, login_default_user):

    clear_model(User)
    create_default_user()
    tokens = login_default_user()
    headers = make_refresh_header(tokens)

    response = client.get(
        path=refresh_url,
        headers=headers,
    )

    assert response.status_code == http.HTTPStatus.OK

    response = client.get(
        path=refresh_url,
        headers=headers,
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED


def test_refresh_without_headers(client, refresh_url):

    response = client.get(
        path=refresh_url,
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
