from http import HTTPStatus


def test_sample(client, test_url):
    response = client.get(
        path=test_url
    )

    assert response.status_code == HTTPStatus.OK

def test_sample_jwt(client, test_jwt_url):
    response = client.get(
        path=test_jwt_url
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
