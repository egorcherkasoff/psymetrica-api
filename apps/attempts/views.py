from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.options.models import Option, OptionScore
from apps.scales.models import Scale
from apps.tests.models import Test

from .exceptions import (
    CantAddAnswersForOthersAttempts,
    CantAttemptDeletedTest,
    CantChangeFinishedAttempt,
    CantUpdateAttempts,
    CantViewAttemptForOthersTests,
)
from .models import Attempt, AttemptAnswer
from .permissions import IsAttemptStarter
from .serializers import (
    AnswerCreateSerializer,
    AnswerSerializer,
    AttemptCreateSerializer,
    AttemptDetailSerializer,
    AttemptListSerializer,
)


class StartAttempt(generics.CreateAPIView):
    """эндпоинт для старта попытки"""

    serializer_class = AttemptCreateSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self, id):
        try:
            test = Test.objects.get(id=id, is_published=True, deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует, или он не является публичным")
        return test

    def create(self, request, *args, **kwargs):
        id = request.data.get("attempt_test")
        test = self.get_object(id)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(test=test, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class AddAttemptAnswer(generics.CreateAPIView):
    """эндпоинт добавления ответа попытке"""

    serializer_class = AnswerCreateSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAttemptStarter,
    ]

    def get_object(self, id):
        try:
            attempt = Attempt.objects.get(
                id=id, user=self.request.user, finished__isnull=True
            )
        except Attempt.DoesNotExist:
            raise NotFound("Такой попытки не существует")
        self.check_object_permissions(self.request, attempt)
        return attempt

    def create(self, request, id, *args, **kwargs):
        attempt = self.get_object(id)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(attempt=attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
