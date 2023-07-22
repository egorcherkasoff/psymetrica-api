from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import CantAssignTests, CantAssignTestsForYourself, NotYourTest
from .models import Test
from .pagination import TestPagination
from .renderers import TestJSONRenderer, TestsJSONRenderer
from .serializers import (
    TestCreateSerializer,
    TestDetailSerializer,
    TestListSerializer,
    TestUpdateSerializer,
)

User = get_user_model()


class TestListAPIView(generics.ListAPIView):
    """постраничный вывод тестов"""

    serializer_class = TestListSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Test.objects.filter(deleted_at__isnull=True)
    renderer_classes = (TestsJSONRenderer,)
    pagination_class = TestPagination


class TestDetailAPIView(generics.RetrieveAPIView):
    """возвращает один тест по slug полю"""

    serializer_class = TestDetailSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    renderer_classes = (TestJSONRenderer,)

    def retrieve(self, request, slug, *args, **kwargs):
        try:
            test = Test.objects.get(slug=slug, deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Test with following url doesnt exist.")
        serializer = self.serializer_class(test, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestCreateAPIView(generics.CreateAPIView):
    """создает тест"""

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = TestCreateSerializer
    renderer_classes = (TestJSONRenderer,)

    def post(self, request, *args, **kwargs):
        serialiser = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serialiser.is_valid(raise_exception=True):
            serialiser.save(author=request.user)
        return Response(serialiser.data, status=status.HTTP_201_CREATED)


class TestUpdateAPIView(generics.UpdateAPIView):
    """обновление данных теста по slug"""

    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (TestJSONRenderer,)
    serializer_class = TestUpdateSerializer

    def patch(self, request, slug, *args, **kwargs):
        try:
            # check
            test = Test.objects.get(slug=slug, deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Test with following url doesnt exist.")

        user = request.user
        if test.author != user:
            raise NotYourTest

        data = request.data
        serializer = TestUpdateSerializer(instance=test, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestDestroyAPIView(generics.DestroyAPIView):
    """удаляет один тест по slug"""

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def destroy(self, request, slug):
        try:
            test = Test.objects.get(slug=slug, deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Test with following url doesnt exist.")

        if test.author != request.user:
            raise NotYourTest

        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
