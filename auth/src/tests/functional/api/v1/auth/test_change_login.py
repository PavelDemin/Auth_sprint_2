import http

from app.models.user import User


def test_change_login_ok(client, change_login_url, make_access_header, login_user, login, password,
                         clear_model, create_default_user, login_default_user):

    clear_model(User)
    create_default_user()
    tokens = login_default_user()
    headers = make_access_header(tokens)

    new_login = 'new_login'

    response = client.post(
        path=change_login_url,
        headers=headers,
        data={'login': new_login}
    )

    assert response.status_code == http.HTTPStatus.OK

    response = login_user(login=login, password=password)

    assert response.status_code == http.HTTPStatus.UNAUTHORIZED

    response = login_user(login=new_login, password=password)

    assert response.status_code == http.HTTPStatus.OK


def test_change_login_blank_login(client, change_login_url, make_access_header,
                                  clear_model, create_default_user, login_default_user):

    clear_model(User)
    create_default_user()
    tokens = login_default_user()
    headers = make_access_header(tokens)

    response = client.post(
        path=change_login_url,
        headers=headers,
        data={'login': ''}
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST
