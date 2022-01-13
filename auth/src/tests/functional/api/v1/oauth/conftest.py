from urllib.parse import urljoin

import pytest


@pytest.fixture
def login_url(oauth_url):
    return urljoin(oauth_url, 'login/google')

@pytest.fixture
def fake_login_url(oauth_url):
    return urljoin(oauth_url, 'login/fake')

@pytest.fixture
def auth_url(oauth_url):
    return urljoin(oauth_url, 'auth/google')
