from functools import wraps

from flask import request
from marshmallow import ValidationError

from app.exceptions import RequestValidationException


class RequestValidator:

    @classmethod
    def validate_body(cls, schema):

        def func(f):
            @wraps(f)
            def inner(*args, **kwargs):
                try:
                    if request.form:
                        data = schema().load(request.form)
                    elif request.json:
                        data = schema().load(request.json)
                    else:
                        raise RequestValidationException('No body data')
                except ValidationError as e:
                    raise RequestValidationException(e.messages)
                return f(*args, data=data, **kwargs)
            return inner
        return func

    @classmethod
    def validate_path_args(cls, schema):
        def func(f):
            @wraps(f)
            def inner(*args, **kwargs):
                try:
                    if request.args:
                        data = schema().load(request.args)
                    else:
                        raise RequestValidationException('No path parameters')
                except ValidationError as err:
                    raise RequestValidationException(err.messages)
                return f(*args, data=data, **kwargs)
            return inner
        return func

    @classmethod
    def validate_path_parameters(cls, schema):
        def func(f):
            @wraps(f)
            def inner(*args, **kwargs):
                try:
                    if request.view_args:
                        __ = schema().load(request.view_args)
                    else:
                        raise RequestValidationException('No path parameters')
                except ValidationError as err:
                    raise RequestValidationException(err.messages)
                return f(*args, **kwargs)
            return inner
        return func
