from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """проверка на владение объектом теста"""

    def has_object_permission(self, request, view, obj):
        if request.METHOD == permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
