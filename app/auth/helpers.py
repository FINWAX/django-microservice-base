import time

import requests
from requests.auth import HTTPBasicAuth
from authlib.jose import jwt
from authlib.oauth2 import OAuth2Error

from msvc.settings import AUTH_JWT_PRIVATE_KEY_FILE, AUTH_DOMAIN, FINWAX_PROJECT_ID, AUTH_INTROSPECTION_URL, \
    AUTH_BASIC_CLIENT_ID, AUTH_BASIC_CLIENT_SECRET, AUTH_JWT_KEY_ALGORITHM


def gen_user_token_cache_key(token):
    """
    Сгенерировать ключ кеша для результата интроспекции токена пользователя.
    :param token: Bearer Token.
    :return: Ключ кэша.
    """
    return 'bearerToken_' + str(token)


def introspect_token_via_jwt_auth(token):
    """
    Провести интроспекцию токена пользователя, используя аутентификацию с помощью JWT.
    :param token: Bearer Token.
    :return: Результат интроспекции.
    """
    if not AUTH_INTROSPECTION_URL:
        return None

    jwt_token = gen_auth_app_jwt_token()
    if not jwt_token:
        return None

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": jwt_token,
        "token": token,
    }
    response = requests.post(
        AUTH_INTROSPECTION_URL, headers=headers, data=data
    )
    response.raise_for_status()

    return response.json()


def introspect_token_via_basic_auth(token):
    """
    Провести интроспекцию токена пользователя, используя аутентификацию с помощью basic auth.
    :param token: Bearer Token.
    :return: Результат интроспекции.
    """
    if not AUTH_INTROSPECTION_URL:
        return None

    data = {'token': token, 'token_type_hint': 'access_token', 'scope': 'openid'}
    auth = HTTPBasicAuth(AUTH_BASIC_CLIENT_ID, AUTH_BASIC_CLIENT_SECRET)
    resp = requests.post(AUTH_INTROSPECTION_URL, data=data, auth=auth)
    resp.raise_for_status()
    return resp.json()


def validate_introspected_token(token, scopes, request):
    """
    Проверить результат интроспекции токена.
    :param token: Результат интроспекции токена.
    :param scopes: Требуемые разрешения.
    :param request: Запрос.
    """
    if not token:
        raise OAuth2Error(
            error="invalid_token_revoked",
            description="Token was revoked.",
            status_code=200
        )
    if not token.get("active", None):
        raise OAuth2Error(
            error='token_invalid',
            description="Token is invalid",
            status_code=200
        )
    now = int(time.time())
    if token["exp"] < now:
        raise OAuth2Error(
            error="invalid_token_expired",
            description="Token has expired.",
            status_code=200
        )


def gen_self_auth_jwt_token() -> None | str:
    """
    Создать JWT токен для аутентификации сервиса.
    :return: Строка JWT токена, либо None.
    """
    jwt_token = gen_auth_app_jwt_token()
    if not jwt_token:
        return None

    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "scope": f"openid profile email urn:zitadel:iam:org:project:id:{FINWAX_PROJECT_ID}:aud read:messages",
        "assertion": jwt_token
    }

    if not AUTH_DOMAIN:
        return None
    url = f'{AUTH_DOMAIN.rstrip('/')}/oauth/v2/token'
    response = requests.post(url, data=data)

    if response.status_code == 200:
        dec_resp = response.json()
        return dec_resp.get('access_token', None)

    return None


def gen_auth_app_jwt_token():
    """
    Сгенерировать JWT токен для подтверждения сервиса.
    :return: JWT токен.
    """
    if not AUTH_JWT_PRIVATE_KEY_FILE:
        return None

    if not AUTH_DOMAIN or not AUTH_JWT_PRIVATE_KEY_FILE:
        return None
    payload = {
        "iss": AUTH_JWT_PRIVATE_KEY_FILE["clientId"],
        "sub": AUTH_JWT_PRIVATE_KEY_FILE["clientId"],
        "aud": AUTH_DOMAIN,
        "exp": int(time.time()) + 60 * 60,  # Expires in 1 hour
        "iat": int(time.time()),
    }
    header = {"alg": AUTH_JWT_KEY_ALGORITHM, "kid": AUTH_JWT_PRIVATE_KEY_FILE["keyId"]}
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
