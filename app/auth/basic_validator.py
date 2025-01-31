import time

from authlib.oauth2 import OAuth2Error
from authlib.oauth2.rfc7662 import IntrospectTokenValidator
import requests
from requests.auth import HTTPBasicAuth

from msvc.settings import AUTH_INTROSPECTION_URL, AUTH_BASIC_CLIENT_ID, AUTH_BASIC_CLIENT_SECRET


class BasicZitadelIntrospectTokenValidator(IntrospectTokenValidator):
    def introspect_token(self, token_string):
        url = AUTH_INTROSPECTION_URL
        data = {'token': token_string, 'token_type_hint': 'access_token', 'scope': 'openid'}
        auth = HTTPBasicAuth(AUTH_BASIC_CLIENT_ID, AUTH_BASIC_CLIENT_SECRET)
        resp = requests.post(url, data=data, auth=auth)
        resp.raise_for_status()
        return resp.json()

    def validate_token(self, token, scopes, request):
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

    def __call__(self, *args, **kwargs):
        res = self.introspect_token(*args, **kwargs)
        return res
