from django.urls import include, path
from rest_framework import routers

from app import views
from app.views import unprotected_hello, protected_hello, health_availability, health_check

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'plugs', views.PlugViewSet)

urlpatterns = [
    path('health/check', health_check),
    path('health/availability', health_availability),
    path('greeting/hello-unprotected', unprotected_hello),
    path('greeting/hello-protected', protected_hello),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
