from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from ..tests.models import Test
from .exceptions import (
    CantAddQuestionsForOthersTest,
    CantDeleteQuestionsForOthersTest,
    CantUpdateQuestionsForOthersTest,
    IncorrectQuestionNumber,
    QuestionNotForThisTest,
    QuestionWithNumberExists,
)
from .models import Question
from .serializers import QuestionCreateUpdateSerializer, QuestionSerializer

User = get_user_model()


def check_question_number(test, number):
    """проверяет правильность введенного номера вопроса"""
    if number > test.questions.count() + 1:
        raise IncorrectQuestionNumber


class TestQuestionsListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = QuestionSerializer

    def get_queryset(self):
        slug = self.kwargs.get("test_slug")
        try:
            test = Test.objects.get(slug=slug)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует.")
        return test.questions.filter(deleted_at__isnull=True)


class QuestionCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для создания вопроса"""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = QuestionCreateUpdateSerializer

    def post(self, request, test_slug, *args, **kwargs):
        try:
            test = Test.objects.get(slug=test_slug)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует.")

        if test.author != request.user:
            raise CantAddQuestionsForOthersTest

        question_number = request.data.get("number")

        if test.questions.filter(number=question_number).exists():
            raise QuestionWithNumberExists

        check_question_number(test, question_number)

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(test=test)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuestionUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт для обновления вопроса"""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = QuestionCreateUpdateSerializer

    def patch(self, request, test_slug, id, *args, **kwargs):
        try:
            test = Test.objects.get(slug=test_slug)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует.")
        try:
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            raise NotFound("Такого вопроса не существует.")

        if question.test != test:
            raise QuestionNotForThisTest

        if test.author != request.user:
            raise CantUpdateQuestionsForOthersTest

        serializer = self.serializer_class(
            question, data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionDeleteAPIView(generics.DestroyAPIView):
    """Эндпоинт для удаления вопроса"""

    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, test_slug, question_id, *args, **kwargs):
        try:
            test = Test.objects.get(slug=test_slug)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует.")
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise NotFound("Такого вопроса не существует.")

        if test.author != request.user:
            raise CantDeleteQuestionsForOthersTest

        if question.test != test:
            raise QuestionNotForThisTest

        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
