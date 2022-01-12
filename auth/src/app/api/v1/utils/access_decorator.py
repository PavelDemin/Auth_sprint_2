from functools import wraps
from http import HTTPStatus
from typing import cast

from flask import abort
from flask_jwt_extended import current_user

from app.models.role import DefaultRoleEnum
from app.models.user import User


def admin_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not cast(User, current_user).has_role(DefaultRoleEnum.admin.value):
            return abort(HTTPStatus.FORBIDDEN, description=f'Only for {DefaultRoleEnum.admin.value}')
        return f(*args, **kwargs)
    return inner
