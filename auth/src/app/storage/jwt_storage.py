from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import cast

from flask_jwt_extended import decode_token, get_jti
from redis import Redis

from app.settings import settings


class JWTStorage(ABC):

    @abstractmethod
    def save_token(self, token: str, user_id: str) -> None:
        pass

    @abstractmethod
    def get_token(self, jti: str, user_id: str) -> str:
        pass

    @abstractmethod
    def remove_token(self, jti: str, user_id: str) -> None:
        pass

    @abstractmethod
    def remove_tokens(self, user_id: str) -> None:
        pass

class JWTRedisStorage(JWTStorage):

    def __init__(self):
        self.redis = Redis.from_url(url=settings.REDIS.DSN, decode_responses=True)

    @staticmethod
    def _get_key(user_id: str, jti: str) -> str:
        return f'{user_id}:{jti}'

    @staticmethod
    def _get_ttl(token: str) -> timedelta:
        token_exp = decode_token(token).get('exp')
        return datetime.fromtimestamp(token_exp) - datetime.now()

    def save_token(self, token: str, user_id: str) -> None:
        jti = get_jti(token)
        key = self._get_key(user_id, jti)
        exp = self._get_ttl(token)
        self.redis.set(key, jti, ex=exp)

    def get_token(self, jti: str, user_id: str) -> str:
        return cast(str, self.redis.get(self._get_key(user_id, jti)))

    def remove_token(self, jti: str, user_id: str) -> None:
        self.redis.delete(self._get_key(user_id, jti))

    def remove_tokens(self, user_id: str) -> None:
        for key in self.redis.scan_iter(self._get_key(user_id, '*')):
            self.redis.delete(key)
