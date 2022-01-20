from authlib.integrations.flask_client import OAuth

from app.settings import settings

from .utils import map_profile_fields


def normalize_userinfo(client, data):
    return map_profile_fields(data, {
        'sub': 'id',
        'name': 'real_name',
        'given_name': 'first_name',
        'family_name': 'last_name',
        'preferred_username': 'login',
        'picture': _get_picture,
        'email': 'default_email',
        'gender': 'sex',
        'birthdate': 'birthday'
    })


def init_yandex(oauth: OAuth):

    oauth.register(
        name='yandex',
        client_id=settings.OAUTH_Yandex.CLIENT_ID,
        client_secret=settings.OAUTH_Yandex.CLIENT_SECRET,
        api_base_url='https://login.yandex.ru/',
        access_token_url='https://oauth.yandex.com/token',
        authorize_url='https://oauth.yandex.com/authorize',
        userinfo_endpoint='info',
        userinfo_compliance_fix=normalize_userinfo,
    )

def _get_picture(data):
    if not data.get('is_avatar_empty', True):
        tpl = 'https://avatars.yandex.net/get-yapic/{}/islands-200'
        return tpl.format(data['default_avatar_id'])
