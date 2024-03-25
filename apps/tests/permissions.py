from rest_framework import permissions


class CanCreateTestsOrNot(permissions.BasePermission):
    """может ли юзер создавать тесты"""

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.has_perm("tests.add_test")


class CanUpdateDeleteTestsOrNot(permissions.BasePermission):
    """может ли юзер обновлять или удалять тесты"""

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.has_perms(["tests.change_test", "tests.delete_test"])

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.author == request.user


class CanAssignTestsOrNot(permissions.BasePermission):
    """может ли юзер назначать тесты"""

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.has_perm("tests.can_assign_tests")


class IsOwnerOrNot(permissions.BasePermission):
    """является ли пользователь владельцем теста"""

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.has_perm("tests.can_assign_tests")

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.author == request.user
