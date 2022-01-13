from authlib.integrations.flask_client import OAuth
from flask import Flask

from .google import init_google
from .yandex import init_yandex

oauth = OAuth()

init_google(oauth)
init_yandex(oauth)

def init_oauth(app: Flask):

    oauth.init_app(app)
