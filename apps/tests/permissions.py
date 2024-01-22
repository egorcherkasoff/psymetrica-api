from rest_framework import permissions


class CanCreateTestsOrNot(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.has_perm("create_test")


class CanUpdateDeleteTestsOrNot(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.has_perms(["update_test", "delete_test"])

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.author == request.user
