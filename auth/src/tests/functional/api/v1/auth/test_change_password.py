import http

from app.models.user import User


def test_change_password_ok(client, change_password_url, make_access_header, login_user, login, password,
                            clear_model, create_default_user, login_default_user):

    clear_model(User)
    create_default_user()
    tokens = login_default_user()
    headers = make_access_header(tokens)

    new_password = 'new_password'

    response = client.post(
        path=change_password_url,
        headers=headers,
        data={'password': new_password}
    )

    assert response.status_code == http.HTTPStatus.OK

    response = login_user(login=login, password=password)

    assert response.status_code == http.HTTPStatus.UNAUTHORIZED

    response = login_user(login=login, password=new_password)

    assert response.status_code == http.HTTPStatus.OK


def test_change_password_blank_password(client, change_password_url, make_access_header,
                                        clear_model, create_default_user, login_default_user):

    clear_model(User)
    create_default_user()
    tokens = login_default_user()
    headers = make_access_header(tokens)

    response = client.post(
        path=change_password_url,
        headers=headers,
        data={'password': ''}
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_change_password_without_headers(client, change_password_url):

    new_password = 'new_password'

    response = client.post(
        path=change_password_url,
        data={'password': new_password}
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
