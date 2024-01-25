from rest_framework.permissions import BasePermission


class IsQuestionTestAuthor(BasePermission):
    """проверка на владение тестом"""

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.has_perm("questions.add_question")

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.author == request.user
