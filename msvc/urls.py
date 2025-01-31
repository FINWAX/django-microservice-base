from django.urls import include, path
from rest_framework import routers

from app import views
from app.views import custom_view_basic, custom_view_jwt

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'plugs', views.PlugViewSet)

urlpatterns = [
    path('custom_basic', custom_view_basic),
    path('custom_jwt', custom_view_jwt),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
