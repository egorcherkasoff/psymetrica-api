from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.tests.models import Test
from .exceptions import (
    CantAddAnswersForOthersAttempts,
    CantAttemptDeletedTest,
    CantChangeFinishedAttempt,
    CantUpdateAttempts,
    CantViewAttemptForOthersTests,
)
from .models import Attempt, AttemptAnswer
from .serializers import AttemptSerializer, AttemptAnswerSerializer


class StartAttemptAPIView(generics.CreateAPIView):
    serializer_class = AttemptSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, test_id, *args, **kwargs):
        try:
            test = Test.objects.get(id=test_id, deleted_at__isnull=True)
        except Test.DoesNotExist:
            raise NotFound

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(test=test, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AttemptRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = AttemptSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        try:
            attempt = Attempt.objects.get(id=self.kwargs["id"])
        except Attempt.DoesNotExist:
            raise NotFound
        if (
            attempt.user != self.request.user
            or attempt.test.author != self.request.user
        ):
            raise CantViewAttemptForOthersTests
        return attempt


class CreateAttemptAnswerCreateAPIView(generics.CreateAPIView):
    serializer_class = AttemptAnswerSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, attempt_id, *args, **kwargs):
        try:
            attempt = Attempt.objects.get(id=attempt_id)
        except Attempt.DoesNotExist:
            raise NotFound("Такой попытки не существует.")

        if attempt.user != self.request.user:
            raise CantAddAnswersForOthersAttempts

        if attempt.is_finished:
            raise CantChangeFinishedAttempt

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(attempt=attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
