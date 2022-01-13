import http


def test_login_fake_service(client, fake_login_url):

    response = client.get(
        path=fake_login_url,
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST
