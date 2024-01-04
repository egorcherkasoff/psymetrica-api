from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from ..tests.models import Test
from .exceptions import (
    CantAddQuestionsForOthersTest,
    CantDeleteQuestionsForOthersTest,
    CantUpdateQuestionsForOthersTest,
    QuestionNotForThisTest,
    QuestionWithNumberExists,
)
from .models import Question
from .renderers import QuestionJSONRenderer
from .serializers import (
    QuestionCreateSerializer,
    QuestionSerializer,
    QuestionUpdateSerializer,
)

User = get_user_model()


class QuestionDetailAPIView(generics.RetrieveAPIView):
    """возвращает один вопрос по slug полю и номеру вопроса"""

    serializer_class = QuestionSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    renderer_classes = (QuestionJSONRenderer,)

    def retrieve(self, request, slug, number, *args, **kwargs):
        try:
            question = Question.objects.get(
                test__slug=slug, number=number, deleted_at__isnull=True
            )
        except Question.DoesNotExist:
            raise NotFound("Question with following number doesnt exist.")
        serializer = self.serializer_class(question, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionCreateAPIView(generics.CreateAPIView):
    """создает вопрос"""

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = QuestionCreateSerializer
    renderer_classes = (QuestionJSONRenderer,)

    def post(self, request, slug, *args, **kwargs):
        test = Test.objects.get(slug=slug)
        if request.user != test.author:
            raise CantAddQuestionsForOthersTest
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            # получем максимальный "номер" для создания нового вопроса
            question_number = Question.objects.last().number + 1
            serializer.save(number=question_number)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuestionUpdateAPIView(generics.UpdateAPIView):
    """обновление данных вопроса по slug теста и номеру вопроса"""

    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (QuestionJSONRenderer,)
    serializer_class = QuestionUpdateSerializer

    def patch(self, request, slug, number, *args, **kwargs):
        try:
            question = Question.objects.get(
                slug=slug, deleted_at__isnull=True, number=number
            )
        except Question.DoesNotExist:
            raise NotFound("Test with following url doesnt exist.")

        if question.test.author != request.user:
            raise CantUpdateQuestionsForOthersTest

        data = request.data
        serializer = QuestionUpdateSerializer(
            instance=question, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestDestroyAPIView(generics.DestroyAPIView):
    """удаляет один тест по slug"""

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def destroy(self, request, slug, number):
        try:
            question = Question.objects.get(
                slug=slug, number=number, deleted_at__isnull=True
            )
        except Test.DoesNotExist:
            raise NotFound("Test with following url doesnt exist.")

        if question.test.author != request.user:
            raise CantDeleteQuestionsForOthersTest

        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
