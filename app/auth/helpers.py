import time
from pprint import pprint

import requests
from authlib.jose import jwt

from msvc import settings
from msvc.settings import AUTH_JWT_PRIVATE_KEY_FILE, AUTH_DOMAIN, FINWAX_PROJECT_ID


def gen_self_auth_jwt_token() -> None | str:
    """
    Создать JWT токен для аутентификации сервиса.
    :return: Строка JWT токена, либо None.
    """
    jwt_token = gen_auth_app_jwt_token()

    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "scope": f"openid profile email urn:zitadel:iam:org:project:id:{FINWAX_PROJECT_ID}:aud read:messages",
        "assertion": jwt_token
    }

    url = f'{AUTH_DOMAIN.rstrip('/')}/oauth/v2/token'
    response = requests.post(url, data=data)

    pprint(response.json())

    if response.status_code == 200:
        dec_resp = response.json()
        return dec_resp.get('access_token', None)

    return None


def gen_auth_app_jwt_token():
    """
    Сгенерировать JWT токен для подтверждения сервиса.
    :return: JWT токен.
    """
    payload = {
        "iss": AUTH_JWT_PRIVATE_KEY_FILE["clientId"],
        "sub": AUTH_JWT_PRIVATE_KEY_FILE["clientId"],
        "aud": settings.AUTH_DOMAIN,
        "exp": int(time.time()) + 60 * 60,  # Expires in 1 hour
        "iat": int(time.time()),
    }
    header = {"alg": settings.AUTH_JWT_KEY_ALGORITHM, "kid": AUTH_JWT_PRIVATE_KEY_FILE["keyId"]}
    return jwt.encode(
        header,
        payload,
        AUTH_JWT_PRIVATE_KEY_FILE["key"],
    )


def get_user(token_string):
    """
    Получить данные пользователя по его токену.
    :param token_string: Строка токена.
    :return: Словарь основных полей пользователя.
    """
    url = f'{AUTH_DOMAIN.rstrip('/')}/oidc/v1/userinfo'
    resp = requests.get(url, headers={'Authorization': 'Bearer ' + token_string})
    resp.raise_for_status()
    return resp.json()
