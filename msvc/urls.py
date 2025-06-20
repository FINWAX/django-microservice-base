from django.urls import include, path
from rest_framework import routers

from app import views
from app.views import unprotected_hello, protected_hello, health_availability, health_check

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'plugs', views.PlugViewSet)

urlpatterns = [
    path('api/health/check', health_check),
    path('api/health/availability', health_availability),

    path('api/v1/greeting/helloUnprotected', unprotected_hello),
    path('api/v1/greeting/helloProtected', protected_hello),
    path('', include(router.urls)),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
