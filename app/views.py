from authlib.integrations.django_oauth2 import ResourceProtector
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import permissions, viewsets

from app.auth.basic_validator import BasicZitadelIntrospectTokenValidator
from app.auth.jwt_validator import JWTZitadelIntrospectTokenValidator
from app.models import Plug
from app.serializers import UserSerializer, PlugSerializer

require_basic_auth = ResourceProtector()
require_basic_auth.register_token_validator(BasicZitadelIntrospectTokenValidator())

require_jwt_auth = ResourceProtector()
require_jwt_auth.register_token_validator(JWTZitadelIntrospectTokenValidator())


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlugViewSet(viewsets.ModelViewSet):
    queryset = Plug.objects.all().order_by('created_at')
    serializer_class = PlugSerializer


# Example of endpoint authenticated by basic auth.
@require_basic_auth()
def custom_view_basic(request):
    output = {
        'token': request.oauth_token
    }

    return JsonResponse(output)


# Example of endpoint authenticated by JWT auth.
@require_jwt_auth()
def custom_view_jwt(request):
    output = {
        'token': request.oauth_token
    }

    return JsonResponse(output)
