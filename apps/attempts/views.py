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
from .serializers import AttemptAnswerSerializer, AttemptSerializer


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

    # TODO: добавить логику запрета ответа на один и тот же вопрос, запрет на ответ если попытка завершена
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
            option_id = serializer.validated_data["option"]["id"]
            option = Option.objects.get(id=option_id)
            try:
                score_obj = option.scores.get(deleted_at__isnull=True)
                score = score_obj.score
                scale = score_obj.scale
            except OptionScore.DoesNotExist:
                score = 1
                scale = None

            serializer.save(
                attempt=attempt,
                option=option,
                score=score,
                scale=scale,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AllTestAttemptsListAPIView(generics.ListAPIView):
    serializer_class = AttemptSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        try:
            test = Test.objects.get(id=self.kwargs["test_id"])
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")
        if test.author != self.request.user:
            raise CantViewAttemptForOthersTests
        return Attempt.objects.filter(test=test)


class UserTestAttemptsListAPIView(generics.ListAPIView):
    serializer_class = AttemptSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        try:
            test = Test.objects.get(id=self.kwargs["test_id"])
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")
        return Attempt.objects.filter(test=test, user=self.request.user)


# class GetAttemptResults(generics.RetrieveAPIView):
#     serializer_class = AttemptSerializer
#     permission_classes = [
#         permissions.IsAuthenticated,
#     ]

#     def get_object(self):
#         raise NotImplementedError
