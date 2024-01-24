from rest_framework import generics, permissions

from apps.tests.filters import TestFilter
from apps.tests.models import AssignedTest, Test
from apps.tests.pagination import TestPagination
from apps.tests.permissions import CanAssignTestsOrNot
from apps.tests.serializers import TestAssignSerializer, TestListSerializer


class UserPublicTests(generics.ListAPIView):
    """Эндпоинт возвращает список публичных тестов пользователя"""

    serializer_class = TestListSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    pagination_class = TestPagination
    filterset_class = TestFilter
    ordering_fields = ("created_at",)

    def get_queryset(self):
        id = self.kwargs.get("id")
        return Test.objects.filter(
            deleted_at__isnull=True, is_published=True, author__id=id
        )


class UserTests(generics.ListAPIView):
    """Эндпоинт возвращает список всех тестов пользователя"""

    serializer_class = TestListSerializer
    permission_classes = [
        permissions.IsAdminUser,
    ]
    pagination_class = TestPagination
    filterset_class = TestFilter
    ordering_fields = ("created_at",)

    def get_queryset(self):
        id = self.kwargs.get("id")
        return Test.objects.filter(deleted_at__isnull=True, author__id=id)


class UserAssignedTests(generics.ListAPIView):
    """Эндпоинт возвращает список назначенных пользователю тестов"""

    serializer_class = TestAssignSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        CanAssignTestsOrNot,
    ]
    ordering_fields = ("created_at",)

    def get_queryset(self):
        id = self.kwargs.get("id")
        return AssignedTest.objects.filter(deleted_at__isnull=True, assigned_to__id=id)
