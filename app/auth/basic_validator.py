from authlib.oauth2.rfc7662 import IntrospectTokenValidator
from django.core.cache import cache

from app.auth.helpers import validate_introspected_token, gen_user_token_cache_key, introspect_token_via_basic_auth
from msvc.settings import AUTH_TOKEN_INTROSPECTION_PERIOD


class BasicZitadelIntrospectTokenValidator(IntrospectTokenValidator):
    def introspect_token(self, token):
        cache_key = gen_user_token_cache_key(token)
        intro = cache.get(cache_key, None)
        if intro is None:
            intro = introspect_token_via_basic_auth(token)
            cache.set(cache_key, intro, AUTH_TOKEN_INTROSPECTION_PERIOD)

        return intro

    def validate_token(self, token, scopes, request):
        validate_introspected_token(token, scopes, request)

    def __call__(self, token, scopes, request):
        token_intro = self.introspect_token(token)
        self.validate_token(token_intro, scopes, request)
        return token_intro
