from authlib.integrations.django_oauth2 import ResourceProtector
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpRequest
from rest_framework import permissions, viewsets

from app.auth.basic_validator import BasicZitadelIntrospectTokenValidator
from app.models import Plug
from app.serializers import UserSerializer, PlugSerializer

require_basic_auth = ResourceProtector()
require_basic_auth.register_token_validator(BasicZitadelIntrospectTokenValidator())


# require_jwt_auth = ResourceProtector()
# require_jwt_auth.register_token_validator(JWTZitadelIntrospectTokenValidator())


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlugViewSet(viewsets.ModelViewSet):
    queryset = Plug.objects.all().order_by('created_at')
    serializer_class = PlugSerializer


# Example of endpoint without user authentication.
def unprotected_hello(request: HttpRequest):
    output = {
        'ok': True,
        'message': f'Hello {request.GET.get('name', 'stranger')}!',
        'token': getattr(request, 'oauth_token', None)
    }

    return JsonResponse(output)


# Example of endpoint authenticated by basic auth.
@require_basic_auth()
def protected_hello(request: HttpRequest):
    output = {
        'ok': True,
        'message': f'Hello {request.GET.get('name', 'stranger')}!',
        'token': getattr(request, 'oauth_token', None)
    }

    return JsonResponse(output)

# # Example of endpoint authenticated by JWT auth.
# @require_jwt_auth()
# def protected_hello(request: HttpRequest):
#     output = {
#         'message': f'Hello {request.GET.get('name', 'stranger')}!',
#         'token': getattr(request, 'oauth_token', None)
#     }
#
#     return JsonResponse(output)

def health_check(request: HttpRequest):
    """
    Check that service is healthy.
    :param request: Запрос.
    :return: Ответ.
    """
    return JsonResponse({
        'ok': True,
    })

def health_availability(request: HttpRequest):
    """
    Check that service is available.
    :param request: Запрос.
    :return: Ответ.
    """
    return JsonResponse({
        'ok': True,
    })

