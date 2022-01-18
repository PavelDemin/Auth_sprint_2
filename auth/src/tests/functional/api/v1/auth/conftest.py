from urllib.parse import urljoin

import pytest
from werkzeug.datastructures import Headers


@pytest.fixture
def logout_url(auth_url):
    return urljoin(auth_url, 'logout')


@pytest.fixture
def logout_all_url(auth_url):
    return urljoin(auth_url, 'logout_all')


@pytest.fixture
def change_password_url(auth_url):
    return urljoin(auth_url, 'change_password')


@pytest.fixture
def change_login_url(auth_url):
    return urljoin(auth_url, 'change_login')


@pytest.fixture
def refresh_url(auth_url):
    return urljoin(auth_url, 'refresh')


@pytest.fixture
def history_url(auth_url):
    return urljoin(auth_url, 'history')


@pytest.fixture
def test_jwt_url(auth_url):
    return urljoin(auth_url, 'test_jwt')


@pytest.fixture
def test_url(auth_url):
    return urljoin(auth_url, 'test')


@pytest.fixture
def fake_access_header():
    return Headers({
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjQwODM4Mjg0LCJqdGkiOiI2YTQ4YjM0NC00MjE5LTQ0YWMtOTBiNi0xYjIyYzY0OWE0MWYiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiNWQ2MzYwNzItOTZjZS00YWZkLTkzMDgtZjQwNDFjMTA0N2M4IiwibmJmIjoxNjQwODM4Mjg0LCJleHAiOjE2NDA4MzkxODQsInJlZnJlc2hfdG9rZW4iOiJhNDIwY2QyZi0yZjdlLTRhNGMtYTVkMC04YmQxM2IwZDY0YzcifQ.PcEPr2yd606a-PxgCTyTS_Df4WBv9w_dwe1RT_ovbDg'
    })
