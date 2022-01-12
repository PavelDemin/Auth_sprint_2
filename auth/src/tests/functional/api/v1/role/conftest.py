from unittest.mock import ANY
from urllib.parse import urljoin

import pytest


@pytest.fixture
def create_role_url(role_url):
    return urljoin(role_url, 'create_role')


@pytest.fixture
def delete_role_url(role_url):
    return urljoin(role_url, 'delete_role')


@pytest.fixture
def update_role_url(role_url):
    return urljoin(role_url, 'update_role')


@pytest.fixture
def get_roles_url(role_url):
    return urljoin(role_url, 'get_roles')


@pytest.fixture
def get_role_url(role_url):
    return urljoin(role_url, 'get_role')


@pytest.fixture
def assign_role_url(role_url):
    return urljoin(role_url, 'assign_role')


@pytest.fixture
def unassign_role_url(role_url):
    return urljoin(role_url, 'unassign_role')


@pytest.fixture
def fake_role_id():
    return 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'


@pytest.fixture
def fake_user_id():
    return 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'


@pytest.fixture
def wait_response_get_role():
    return {
        'description': ANY,
        'id': ANY,
        'name': ANY,
    }
