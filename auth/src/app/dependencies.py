from flask_injector import request
from injector import singleton

from app.services.jwt_service import JWTService
from app.services.user_service import UserService
from app.storage.jwt_storage import JWTRedisStorage, JWTStorage



def configure(binder):
    
    jwt_storage = JWTRedisStorage()
    binder.bind(interface=JWTStorage, to=jwt_storage, scope=singleton)
    binder.bind(interface=UserService, to=UserService, scope=request)
    binder.bind(interface=JWTService, to=JWTService, scope=request)

