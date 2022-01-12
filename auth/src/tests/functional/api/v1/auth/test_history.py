import http
from unittest.mock import ANY

import pytest

from app.models.auth_history import AuthHistory
from app.models.user import User
from app.settings import settings


@pytest.fixture
def wait_history_body():
    return [{
        'id': ANY,
        'timestamp': ANY,
        'user_agent': ANY,
        'ip_address': ANY,
        'device': ANY,
    },
    ]


def test_history_ok(client, history_url, make_access_header, wait_history_body,
                    clear_model, create_default_user, login_default_user):

    clear_model(User)
    clear_model(AuthHistory)
    create_default_user()
    tokens = login_default_user()
    headers = make_access_header(tokens)

    response = client.get(
        path=history_url,
        headers=headers,
        query_string={'page': 1},
    )

    assert response.status_code == http.HTTPStatus.OK

    result = response.json
    assert result == wait_history_body


def test_history_pagination(client, history_url, make_access_header, wait_history_body,
                            clear_model, create_default_user, login_default_user):

    clear_model(User)
    clear_model(AuthHistory)
    create_default_user()
    tokens = login_default_user()
    headers = make_access_header(tokens)

    page_limit = settings.PAGINATION_PAGE_LIMIT

    for _ in range(page_limit):
        login_default_user()

    response = client.get(
        path=history_url,
        headers=headers,
        query_string={'page': 1},
    )

    assert response.status_code == http.HTTPStatus.OK

    result = response.json
    assert len(result) == page_limit

    response = client.get(
        path=history_url,
        headers=headers,
        query_string={'page': 2},
    )

    assert response.status_code == http.HTTPStatus.OK

    result = response.json
    assert len(result) == 1


def test_history_without_headers(client, history_url):

    response = client.get(
        path=history_url,
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
