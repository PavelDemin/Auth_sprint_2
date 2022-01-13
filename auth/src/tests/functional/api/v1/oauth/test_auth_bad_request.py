import http


def test_auth_bad_request(client, auth_url):

    response = client.get(
        path=auth_url,
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST
