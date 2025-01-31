import time


from authlib.oauth2 import OAuth2Error

from authlib.oauth2.rfc7662 import IntrospectTokenValidator
import requests

from app.auth.helpers import gen_auth_app_jwt_token
from msvc import settings



class JWTZitadelIntrospectTokenValidator(IntrospectTokenValidator):
    def introspect_token(self, token_string):
        jwt_token = gen_auth_app_jwt_token()

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": jwt_token,
            "token": token_string,
        }
        response = requests.post(
            settings.AUTH_INTROSPECTION_URL, headers=headers, data=data
        )
        response.raise_for_status()
        token_data = response.json()

        return token_data

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
        if token.get('exp', 0) < now:
            raise OAuth2Error(
                error="invalid_token_expired",
                description="Token has expired.",
                status_code=200
            )

    def __call__(self, token_string, scopes, request):
        token = self.introspect_token(token_string)
        self.validate_token(token, scopes, request)
        return token
