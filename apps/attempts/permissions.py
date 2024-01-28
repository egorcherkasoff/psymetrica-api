from rest_framework.permissions import BasePermission


class IsAttemptStarter(BasePermission):
    """проверяем, является ли пользователь создателем попытки"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.user == request.user
