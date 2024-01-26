from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.questions.pagination import QuestionPagingation
from apps.questions.serializers import QuestionListSerializer

from .exceptions import CantAssignTestsForYourself
from .filters import TestFilter
from .models import Category, Test
from .pagination import TestPagination
from .permissions import (
    CanAssignTestsOrNot,
    CanCreateTestsOrNot,
    CanUpdateDeleteTestsOrNot,
    IsOwnerOrNot,
)
from .serializers import (
    CategorySerializer,
    TestAssignSerializer,
    TestCreateSerializer,
    TestDetailSerializer,
    TestListSerializer,
    TestUpdateSerializer,
)

User = get_user_model()


class CategoriesList(generics.ListAPIView):
    """Эндпоинт возвращает список категорий"""

    serializer_class = CategorySerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Category.objects.filter(deleted_at__isnull=True)


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
    serializer_class = TestCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            category = None
            if "category" in request.data:
                try:
                    category = Category.objects.get(id=request.data["category"])
                except Category.DoesNotExist:
                    raise NotFound("Такой категории не существует")
            serializer.save(author=request.user, category=category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TestUpdate(generics.UpdateAPIView):
    """Эндпоинт для обновления теста"""

    permission_classes = (
        permissions.IsAuthenticated,
        CanUpdateDeleteTestsOrNot,
    )

    serializer_class = TestUpdateSerializer

    def get_object(self, slug):
        try:
            test = Test.objects.get(slug=slug, deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")
        self.check_object_permissions(self.request, test)
        return test

    def patch(self, request, slug, *args, **kwargs):
        test = self.get_object(slug)
        serializer = self.serializer_class(
            instance=test, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestDelete(generics.DestroyAPIView):
    """Эндпоинт для удаления теста"""

    permission_classes = [
        permissions.IsAuthenticated,
        CanUpdateDeleteTestsOrNot,
    ]

    def get_object(self, slug):
        try:
            test = Test.objects.get(slug=slug, deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")
        self.check_object_permissions(self.request, test)
        return test

    def destroy(self, request, slug):
        test = self.get_object(slug)
        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssignTest(generics.CreateAPIView):
    """Эндпоинт для назначения теста другому пользователю"""

    permission_classes = [
        permissions.IsAuthenticated,
        CanAssignTestsOrNot,
    ]
    serializer_class = TestAssignSerializer

    def get_object(self, slug):
        try:
            test = Test.objects.get(slug=slug, deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")
        return test

    def post(self, request, slug):
        test = self.get_object(slug)
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            try:
                user = User.objects.get(id=request.data["assigned_to"])
            except User.DoesNotExist:
                raise NotFound("Такого пользователя не существует")
            if user == request.user:
                raise CantAssignTestsForYourself
            serializer.save(assigned_by=request.user, test=test, assigned_to=user)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class TestAssignsList(generics.ListAPIView):
    """Эндпоинт для получения списка назначенных тестов"""

    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrNot,
    ]
    serializer_class = TestAssignSerializer

    def get_object(self):
        try:
            test = Test.objects.get(slug=self.kwargs["slug"], deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")
        return test

    def get_queryset(self):
        test = self.get_object()
        self.check_object_permissions(self.request, test)
        return test.assignments.filter(deleted_at__isnull=True)


class TestQuestionsList(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = QuestionListSerializer
    pagination_class = QuestionPagingation

    def get_queryset(self):
        try:
            test = Test.objects.get(slug=self.kwargs["slug"], deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")
        return test.questions
