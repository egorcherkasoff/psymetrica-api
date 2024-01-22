from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import CantAssignTests, CantAssignTestsForYourself, NotYourTest
from .models import AssignedTest, Test
from .pagination import TestPagination
from .permissions import CanCreateTestsOrNot, CanUpdateDeleteTestsOrNot
from .serializers import (
    TestCreateUpdateSerializer,
    TestDetailSerializer,
    TestListSerializer,
)
from .filters import TestFilter

User = get_user_model()


class PublicTestList(generics.ListAPIView):
    """Эндпоинт выводит список всех публчиных тестов"""

    serializer_class = TestListSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Test.objects.filter(deleted_at__isnull=True, is_published=True)
    pagination_class = TestPagination
    filterset_class = TestFilter
    ordering_fields = ("created_at",)


class PublicTestDetail(generics.RetrieveAPIView):
    """Эндпоинт возвращает один публичный тест по его slug"""

    serializer_class = TestDetailSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def retrieve(self, request, slug, *args, **kwargs):
        try:
            test = Test.objects.get(
                slug=slug, deleted_at__isnull=True, is_published=True
            )
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует.")
        serializer = self.serializer_class(test, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestCreate(generics.CreateAPIView):
    """Эндпоинт для создания теста"""

    permission_classes = [
        permissions.IsAuthenticated,
        CanCreateTestsOrNot,
    ]
    serializer_class = TestCreateUpdateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TestUpdate(generics.UpdateAPIView):
    """Эндпоинт для обновления теста"""

    permission_classes = (
        permissions.IsAuthenticated,
        CanUpdateDeleteTestsOrNot,
    )
    serializer_class = TestCreateUpdateSerializer

    def patch(self, request, slug, *args, **kwargs):
        try:
            test = Test.objects.get(slug=slug, deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")

        data = request.data
        serializer = self.serializer_class(instance=test, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestDelete(generics.DestroyAPIView):
    """Эндпоинт для удаления теста"""

    permission_classes = [
        permissions.IsAuthenticated,
        CanUpdateDeleteTestsOrNot,
    ]

    def destroy(self, request, slug):
        try:
            test = Test.objects.get(slug=slug, deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")

        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssignTest(APIView):
    """назначает тест другому пользователю"""

    # TODO: добавить для модели permission для назначения теста
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, slug, user_id):
        try:
            test = Test.objects.get(slug=slug, deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")

        try:
            user = User.objects.get(id=user_id, deleted_at__isnull=True)
        except User.DoesNotExist:
            raise NotFound("Такого пользователя не существует")

        if user == request.user:
            raise CantAssignTestsForYourself

        AssignedTest.objects.create(
            assigned_by=request.user, assigned_to=user, test=test
        )

        return Response(
            data={"detail": "Тест успешно назначен"}, status=status.HTTP_201_CREATED
        )


class TestsAssignedToUserListAPIView(generics.ListAPIView):
    """Выводит список назначенных пользователю тестов"""

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = TestListSerializer
    pagination_class = TestPagination

    def get_queryset(self):
        return Test.objects.filter(
            assignments__assigned_to__id=self.kwargs.get("user_id"),
            deleted_at__isnull=True,
        )
