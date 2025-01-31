from django.contrib.auth.models import User
from rest_framework import serializers

from app.models import Plug


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class PlugSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plug
        fields = ['name', 'created_at']