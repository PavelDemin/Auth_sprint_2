import json
from abc import ABC
from http import HTTPStatus
from typing import Any, cast

from flask import Flask
from flask.wrappers import Response
from werkzeug.exceptions import HTTPException


class BaseHTTPException(ABC, HTTPException):
    code: HTTPStatus
    name: str

    def __init__(self, description: str):
        self.description = description
        super().__init__()


class RequestValidationException(BaseHTTPException):
    code = HTTPStatus.BAD_REQUEST
    name = 'Error occurred while validating the data in the request'


class ModelSchemaValidationException(BaseHTTPException):
    code = HTTPStatus.CONFLICT
    name = 'Inappropriate data'


class DataBaseException(BaseHTTPException):
    code = HTTPStatus.BAD_REQUEST
    name = 'Occuerred exceptions while working with data'

class WrongCredentialsException(BaseHTTPException):
    code = HTTPStatus.UNAUTHORIZED
    name = 'Wrong login or password'


class InvalidRefreshTokenException(BaseHTTPException):
    code = HTTPStatus.UNAUTHORIZED
    name = 'Refresh token is invalid'


class TooManyRequestsExceptions(BaseHTTPException):
    code = HTTPStatus.TOO_MANY_REQUESTS
    name = 'To many requests'



def init_error_handler(app: Flask):

    class AppResponseAfterValidation(Response, ABC):
        data: Any

    @app.errorhandler(BaseHTTPException)  # type: ignore
    def json_exc_handler(exception: BaseHTTPException):
        resp = cast(AppResponseAfterValidation, exception.get_response())
        resp.data = json.dumps({
            'code': exception.code,
            'name': exception.name,
            'description': exception.description
        })
        resp.content_type = 'application/json'
        return resp
