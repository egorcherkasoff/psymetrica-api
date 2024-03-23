from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(read_only=True, source="get_avatar")
    name = serializers.CharField(read_only=True, source="__str__")

    class Meta:
        model = User
        fields = ["id", "name", "avatar"]


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "email", "password"]
