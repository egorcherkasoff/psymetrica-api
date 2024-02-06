from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    avatar = serializers.CharField(read_only=True, source="get_avatar")

    class Meta:
        model = User
        fields = ["id", "full_name", "avatar"]

    def get_full_name(self, obj):
        return obj.get_full_name


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "email", "password"]
