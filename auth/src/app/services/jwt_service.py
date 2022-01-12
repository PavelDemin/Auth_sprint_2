from typing import Any, Optional, cast

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                current_user, get_jti, get_jwt)
from injector import inject

from app.models.user import User
from app.storage.jwt_storage import JWTStorage


class JWTService:

    @inject
    def __init__(self, storage: JWTStorage):
        self.storage = storage

    @staticmethod
    def get_claim_from_token(claim: str) -> str:
        return get_jwt().get(claim)

    def gen_tokens(self, user: User, fresh: bool = False) -> tuple[str, str]:
        refresh_token = create_refresh_token(user)

        access_claims = {'refresh_token': get_jti(refresh_token), 'user_roles': user.get_roles()}
        access_token = create_access_token(identity=user, fresh=fresh, additional_claims=access_claims)

        return access_token, refresh_token

    def save_refresh_token(self, token: str, user_id) -> None:
        self.storage.save_token(token=token, user_id=user_id)

    def remove_refresh_token(self, jti: str, user_id: str) -> None:
        self.storage.remove_token(jti=jti, user_id=user_id)

    def remove_refresh_tokens(self, user_id: str) -> None:
        self.storage.remove_tokens(user_id=user_id)

    def is_exists_refresh_token(self, jti, user_id: str) -> bool:
        refresh_token = self.storage.get_token(jti=jti, user_id=user_id)
        return bool(refresh_token)
