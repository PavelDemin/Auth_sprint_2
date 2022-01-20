from authlib.integrations.flask_client import OAuth

from app.settings import settings


def init_google(oauth: OAuth):

    oauth.register(
        name='google',
        client_id=settings.OAUTH_Google.CLIENT_ID,
        client_secret=settings.OAUTH_Google.CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
