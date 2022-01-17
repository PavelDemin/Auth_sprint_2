from http import HTTPStatus
from time import sleep

import pytest
from app.main import app
from app.utils.limiter import LimiterRequests
from flask import Response


@pytest.fixture()
def test_path():
    return '/test'


def test_ratelimit(client, test_path, clear_redis):

    @app.route(test_path)
    @LimiterRequests(rate=1)
    def limited_function() -> Response:
        return Response()

    clear_redis()

    for _ in range(10):
        response = client.get(
            path=test_path
        )
        assert response.status_code == HTTPStatus.OK
        response = client.get(
            path=test_path
        )
        assert response.status_code == HTTPStatus.TOO_MANY_REQUESTS

        sleep(1)
