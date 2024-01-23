from rest_framework import permissions


class CanCreateTestsOrNot(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.has_perm("tests.add_test")


class CanUpdateDeleteTestsOrNot(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.has_perms(["tests.change_test", "tests.delete_test"])

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.author == request.user


class CanAssignTestsOrNot(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.has_perm("tests.can_assign_tests")
