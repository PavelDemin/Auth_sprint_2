from typing import Optional, cast

from pydantic import BaseSettings, Field, PostgresDsn, RedisDsn, validator


class WSGISettings(BaseSettings):
    """
    Config for running the app. Not used in main app config.
    """

    app: str = 'app.main:app'
    HOST: str = '0.0.0.0'
    PORT: int = 8001
    reload: bool = False
    workers: int = 3


class RedisSettings(BaseSettings):
    HOST: str = '127.0.0.1'
    PORT: int = 6379
    PROTOCOL: str = 'redis'
    DSN: Optional[RedisDsn] = None

    @validator('DSN', pre=True)
    def build_dsn(cls, v, values) -> RedisDsn:
        if v:
            return v

        protocol = values['PROTOCOL']
        host = values['HOST']
        port = values['PORT']

        return cast(RedisDsn, f'{protocol}://{host}:{port}/')

    class Config:
        env_prefix = 'REDIS_'


class DatabaseSettings(BaseSettings):
    SCHEMA: str = 'auth'

    USER: str = 'postgres'
    PASSWORD: str = 'YzX2oMILuA'
    PORT: str = '5432'
    HOST: str = '127.0.0.1'
    PROTOCOL: str = 'postgresql'
    DSN: Optional[PostgresDsn] = None

    @validator('DSN', pre=True)
    def build_dsn(cls, v, values) -> PostgresDsn:
        if v:
            return v

        protocol = values['PROTOCOL']
        user = values['USER']
        passwd = values['PASSWORD']
        host = values['HOST']
        port = values['PORT']

        return cast(PostgresDsn, f'{protocol}://{user}:{passwd}@{host}:{port}')

    class Config:
        env_prefix = 'POSTGRES_'

class SwaggerSettings(BaseSettings):
    URL: str = Field('/openapi/docs')
    JSON_URL: str = Field('/openapi/swagger.json')

    class Config:
        env_prefix = 'SWAGGER_'

class OAUTH_Google(BaseSettings):

    CLIENT_ID: str = '963136681289-tkqudjg0d6b7rqdcmdqdtnqqoiqk7d33.apps.googleusercontent.com'
    CLIENT_SECRET: str = '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'

    class Config:
        env_prefix = 'OAUTH_GOOGLE_'

class OAUTH_Yandex(BaseSettings):

    CLIENT_ID: str = '065b8a86d02b429e8f3b28a8d63603bf'
    CLIENT_SECRET: str = '1a65d56a23b04c3597d8c6fb54d0636d'

    class Config:
        env_prefix = 'OAUTH_YANDEX_'

class CommonSettings(BaseSettings):
    FLASK_APP: str = 'app.main:app'

    DEBUG: bool = False
    LOG_LEVEL: str = 'INFO'
    SECRET_KEY: str = 'my-32-character-ultra-secure-and-ultra-long-secret'

    TESTING: bool = False

    WSGI: WSGISettings = WSGISettings()
    REDIS: RedisSettings = RedisSettings()
    DB: DatabaseSettings = DatabaseSettings()
    SWAGGER: SwaggerSettings = SwaggerSettings()

    OAUTH_Google: OAUTH_Google = OAUTH_Google()
    OAUTH_Yandex: OAUTH_Yandex = OAUTH_Yandex()

    PAGINATION_PAGE_LIMIT: int = 5

    DEFAULT_ADMIN_LOGIN: str = 'admin'
    DEFAULT_ADMIN_PASSWORD: str = 'admin'
    DEFAULT_ADMIN_EMAIL: str = 'admin@admin.ru'

    LIMITER_RATE: str = '100 per minute'
