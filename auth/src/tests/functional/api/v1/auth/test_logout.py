import http

from app.models.user import User


def test_logout_ok(client, logout_url, make_access_header,
                   clear_model, create_default_user, login_default_user):

    clear_model(User)
    create_default_user()
    tokens = login_default_user()
    headers = make_access_header(tokens)

    response = client.get(
        path=logout_url,
        headers=headers,
    )

    assert response.status_code == http.HTTPStatus.OK


def test_logout_double_query(client, logout_url, make_access_header,
                             clear_model, create_default_user, login_default_user):

    clear_model(User)
    create_default_user()
    tokens = login_default_user()

    _ = client.get(
        path=logout_url,
        headers=make_access_header(tokens),
    )

    response = client.get(
        path=logout_url,
        headers=make_access_header(tokens),
    )

    assert response.status_code == http.HTTPStatus.UNAUTHORIZED


def test_logout_fake_token(client, logout_url, fake_access_header,
                           clear_model, create_default_user):

    clear_model(User)
    create_default_user()

    response = client.get(
        path=logout_url,
        headers=fake_access_header,
    )

    assert response.status_code == http.HTTPStatus.UNAUTHORIZED


def test_logout_without_headers(client, logout_url):

    response = client.get(
        path=logout_url,
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
