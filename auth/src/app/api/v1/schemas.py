from flask_marshmallow.schema import Schema
from marshmallow import fields, validate

login_validate = [validate.Length(min=5, max=50)]
password_validate = [validate.Length(min=5, max=25)]
name_validate = [validate.Length(max=250)]
page_validate = [validate.Range(min=1, error='Value must be greater than 0')]


class LoginSchema(Schema):
    login = fields.String(required=True, validate=login_validate)
    password = fields.String(required=True, validate=password_validate)


class SignUpSchema(Schema):
    login = fields.String(required=True, validate=login_validate)
    password = fields.String(required=True, load_only=True, validate=password_validate)
    first_name = fields.String(validate=name_validate)
    last_name = fields.String(validate=name_validate)
    email = fields.Email()


class UserResponseSchema(Schema):
    id = fields.UUID()
    login = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()


class JWTResponseSchema(Schema):
    access_token = fields.String()
    refresh_token = fields.String()


class ChangePasswordSchema(Schema):
    password = fields.String(required=True, load_only=True, validate=password_validate)


class ChangeLoginSchema(Schema):
    login = fields.String(required=True, validate=login_validate)


class RolesSchema(Schema):
    name = fields.String(required=True, validate=name_validate)
    description = fields.String()


class DeleteRoleSchema(Schema):
    id = fields.UUID()


class ResponseRoleSchema(Schema):
    id = fields.UUID()
    name = fields.String(required=True, validate=name_validate)
    description = fields.String()


class AuthHistorySchema(Schema):
    id = fields.UUID()
    timestamp = fields.DateTime()
    user_agent = fields.String()
    ip_address = fields.String()
    device = fields.String()


class PaginationSchema(Schema):
    page = fields.Int(required=True, validate=page_validate)


class AssignRoleSchema(Schema):
    user_id = fields.UUID(required=True)
    role_id = fields.UUID(required=True)


class UnassignRoleSchema(Schema):
    user_id = fields.UUID(required=True)
    role_id = fields.UUID(required=True)
