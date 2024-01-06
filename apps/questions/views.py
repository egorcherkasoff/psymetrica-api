from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from apps.base.services import sort_by_number, validate_image

from ..tests.models import Test
from .exceptions import (
    CantAddQuestionsForOthersTest,
    CantDeleteQuestionsForOthersTest,
    CantUpdateQuestionsForOthersTest,
    IncorrectQuestionNumber,
    QuestionNotForThisTest,
    QuestionWithNumberExists,
)
from .models import Question, QuestionImage
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
    parser_classes = (MultiPartParser,)

    def post(self, request, test_slug, *args, **kwargs):
        try:
            test = Test.objects.get(slug=test_slug)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует.")

        if test.author != request.user:
            raise CantAddQuestionsForOthersTest

        question_number = int(request.data.get("number"))

        # прикрепил ли юзер картинку
        try:
            image_data = request.data.pop("image")[0]
        except AttributeError:
            image_data = None

        if test.questions.filter(number=question_number).exists():
            raise QuestionWithNumberExists

        check_question_number(test, question_number)

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            question = serializer.save(test=test)
            # создаем картинку если картинка была
            if image_data:
                QuestionImage.objects.create(question=question, image=image_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuestionUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт для обновления вопроса"""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = QuestionCreateUpdateSerializer
    parser_classes = (MultiPartParser,)

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

        # прикрепил ли юзер файл с картинкой
        try:
            image_data = request.data.pop("image")[0]
        except AttributeError:
            image_data = None

        serializer = self.serializer_class(
            question, data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # обновляем картинку если картинка была, иначе создаем новую
            if image_data:
                # проверяем, картинку ли прикрепил юзер
                validate_image(image_data)
                current_image = question.images.get(deleted_at__isnull=True)
                if current_image:
                    current_image.image = image_data
                    current_image.save(update_fields=["image"])
                else:
                    QuestionImage.objects.create(question=question, image=image_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionDeleteAPIView(generics.DestroyAPIView):
    """Эндпоинт для удаления вопроса"""

    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, test_slug, id, *args, **kwargs):
        try:
            test = Test.objects.get(slug=test_slug)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует.")
        try:
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            raise NotFound("Такого вопроса не существует.")

        if test.author != request.user:
            raise CantDeleteQuestionsForOthersTest

        if question.test != test:
            raise QuestionNotForThisTest

        # нужен номер удаляемого вопроса, чтобы подогнать номера других
        question_number = question.number

        question.delete()

        # подгоняем номера оставшихся вопросов, чтобы они шли по порядку
        questions = test.questions.filter(
            deleted_at__isnull=True, number__gt=question_number
        )

        sort_by_number(Question, questions, question_number)
        return Response(status=status.HTTP_204_NO_CONTENT)
