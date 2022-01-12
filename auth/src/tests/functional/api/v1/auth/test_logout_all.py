import http

from app.models.user import User


def test_logout_all_ok(client, logout_all_url, make_access_header,
                       clear_model, create_default_user, login_default_user):

    clear_model(User)
    create_default_user()
    tokens_1 = login_default_user()
    tokens_2 = login_default_user()

    response = client.get(
        path=logout_all_url,
        headers=make_access_header(tokens_1),
    )

    assert response.status_code == http.HTTPStatus.OK

    response = client.get(
        path=logout_all_url,
        headers=make_access_header(tokens_2),
    )

    assert response.status_code == http.HTTPStatus.UNAUTHORIZED


def test_logout_all_double_query(client, logout_all_url, make_access_header,
                                 clear_model, create_default_user, login_default_user):

    clear_model(User)
    create_default_user()
    tokens = login_default_user()

    _ = client.get(
        path=logout_all_url,
        headers=make_access_header(tokens),
    )

    response = client.get(
        path=logout_all_url,
        headers=make_access_header(tokens),
    )

    assert response.status_code == http.HTTPStatus.UNAUTHORIZED


def test_logout_all_fake_token(client, logout_all_url, fake_access_header,
                               clear_model, create_default_user):

    clear_model(User)
    create_default_user()

    response = client.get(
        path=logout_all_url,
        headers=fake_access_header,
    )

    assert response.status_code == http.HTTPStatus.UNAUTHORIZED


def test_logout_all_without_headers(client, logout_all_url):

    response = client.get(
        path=logout_all_url,
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
