from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import CantAssignTests, CantAssignTestsForYourself, NotYourTest
from .models import AssignedTest, Test
from .pagination import TestPagination
from .permissions import IsOwner
from .serializers import (
    TestCreateUpdateSerializer,
    TestSerializer,
)

User = get_user_model()


class TestListAPIView(generics.ListAPIView):
    """Эндпоинт выводит список всех тестов"""

    serializer_class = TestSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Test.objects.filter(deleted_at__isnull=True)
    pagination_class = TestPagination


class TestDetailAPIView(generics.RetrieveAPIView):
    """Эндпоинт возвращает один тест по его slug"""

    serializer_class = TestSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def retrieve(self, request, slug, *args, **kwargs):
        try:
            test = Test.objects.get(slug=slug, deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует.")
        serializer = self.serializer_class(test, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для создания теста"""

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = TestCreateUpdateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TestUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт для обновления теста"""

    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )
    serializer_class = TestCreateUpdateSerializer

    def patch(self, request, slug, *args, **kwargs):
        try:
            # check
            test = Test.objects.get(slug=slug, deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")

        user = request.user
        if test.author != user:
            raise NotYourTest

        data = request.data
        serializer = self.serializer_class(instance=test, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт для удаления теста"""

    permission_classes = [
        permissions.IsAuthenticated,
        IsOwner,
    ]

    def destroy(self, request, slug):
        try:
            test = Test.objects.get(slug=slug, deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")

        if test.author != request.user:
            raise NotYourTest

        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TestAssignAPIView(APIView):
    """назначает тест другому пользователю"""

    permission_classes = [
        permissions.IsAuthenticated,
        IsOwner,
    ]

    def post(self, request, slug, user_id):
        try:
            test = Test.objects.get(slug=slug, deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")

        if test.author != request.user:
            raise NotYourTest

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
            data={"message": "Тест успешно назначен"}, status=status.HTTP_201_CREATED
        )


class TestsAssignedToUserListAPIView(generics.ListAPIView):
    """Выводит список назначенных пользователю тестов"""

    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = TestSerializer
    pagination_class = TestPagination

    def get_queryset(self):
        return Test.objects.filter(
            assignments__assigned_to__id=self.kwargs.get("user_id"),
            deleted_at__isnull=True,
        )
