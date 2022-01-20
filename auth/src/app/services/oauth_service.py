from uuid import uuid4

from flask import jsonify, request
from flask.wrappers import Response
from injector import inject
from sqlalchemy.exc import DatabaseError, SQLAlchemyError

from app.exceptions import DataBaseException
from app.logging import get_logger
from app.models.auth_history import AuthHistory
from app.models.user import OAuthUser, OAuthUserSchema, User
from app.services.jwt_service import JWTService
from app.services.user_service import UserService
from app.storage.db import db
from app.utils.oauth import oauth


class OAuthService():

    model = OAuthUser
    schema = OAuthUserSchema

    @staticmethod
    def _add_auth_history(user: User) -> None:
        ip_address = request.remote_addr
        user_agent = request.user_agent.string

        auth_history = AuthHistory(
            user_id=user.id,
            user_agent=user_agent,
            ip_address=ip_address,
            device=AuthHistory.user_agent_to_user_device(user_agent)
        )
        db.session.add(auth_history)
        try:
            db.session.commit()
        except SQLAlchemyError as exception:
            get_logger().error(f'Ошибка записи истории аутификаций {str(exception)}')

    @inject
    def __init__(self, user_service: UserService, token_service: JWTService):
        self.user_service = user_service
        self.token_service = token_service

    def _create_oauth_user(self, data: dict) -> OAuthUser:

        self.schema().load(data)

        oauth_user = self.model(**data)

        db.session.add(oauth_user)

        try:
            db.session.commit()

        except DatabaseError as exception:
            get_logger().error(exception)
            raise DataBaseException('')
        else:
            return oauth_user

    def authorize_redirect(self, redirect_url: str, service: str):
        client = oauth.create_client(service)
        return client.authorize_redirect(redirect_url)  # type: ignore

    def auth(self, service: str) -> Response:
        client = oauth.create_client(service)

        token = client.authorize_access_token()  # type: ignore
        user_info = token.get('userinfo')

        if not user_info:
            user_info = client.userinfo(token=token)  # type: ignore

        email = user_info['email']
        id = user_info['sub']
        first_name = user_info['given_name']
        last_name = user_info['family_name']

        oauth_user = OAuthUser.query.filter_by(oauth_id=id, oauth_name=service).first()

        if not oauth_user:

            user = self.user_service.get_by_email(email)

            if not user:
                user = self.user_service.create_user(data={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'login': f'auth_{service}_{id}',
                    'password': str(uuid4())
                })

            oauth_user = self._create_oauth_user(data={
                'user_id': user.id,
                'oauth_id': id,
                'oauth_name': service
            })
        else:
            user = self.user_service.get_by_id(oauth_user.user_id)

        access_token, refresh_token = self.token_service.gen_tokens(user, True)
        self.token_service.save_refresh_token(token=refresh_token, user_id=user.id)

        self._add_auth_history(user)

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        })
