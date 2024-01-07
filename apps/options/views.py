from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.base.services import sort_by_number

from .exceptions import (
    CantAddOptionsForOthersTest,
    CantDeleteOptionsForOthersTest,
    CantUpdateOptionsForOthersTest,
    IncorrectOptionNumber,
    IncorrectOptionType,
    OptionNotForThisQuestion,
    OptionTypeOpenMustBeUnique,
    OptionWithNumberExists,
)
from apps.questions.models import Question
from .models import Option, OptionScore
from .serializers import OptionCreateUpdateSerializer, OptionSerializer


def check_option_number(question, number):
    """проверяет правильность введенного номера вопроса"""
    if number > question.options.count() + 1:
        raise IncorrectOptionNumber


class QuestionOptionsListAPIView(generics.ListAPIView):
    """Возвращает список вариантов ответа для определенного вопроса"""

    serializer_class = OptionSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        question_id = self.kwargs.get("question_id")
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise NotFound("Такого вопроса не существует.")
        return question.options.filter(deleted_at__isnull=True)


class OptionCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для создания варианта ответа для вопроса"""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OptionCreateUpdateSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, question_id, *args, **kwargs):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise NotFound("Такого вопроса не существует")

        # является ли юзер владельцем теста
        if question.test.author != request.user:
            raise CantAddOptionsForOthersTest

        if question.options.filter(type=4).exists():
            OptionTypeOpenMustBeUnique

        number = request.data.get("number")

        if not number:
            raise IncorrectOptionNumber
        # проверяем существует ли option с таким номером
        if question.options.filter(number=number).exists():
            raise OptionWithNumberExists

        # чекаем, чтобы номер не был больше количества вариантов
        check_option_number(question, number)

        # проверяем добавил ли пользователь разбалловку или шкалу
        try:
            score = request.data.pop("score")
        except AttributeError:
            score = None
        try:
            scale = request.data.pop("scale")
        except AttributeError:
            scale = None

        serializer = self.serializer_class(
            data=request.data, context={"request": request, "question_id": question_id}
        )
        if serializer.is_valid(raise_exception=True):
            option = serializer.save(question=question)
            if score or scale:
                OptionScore.objects.create(option=option, score=score, scale=scale)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class OptionUpdateAPIView(generics.UpdateAPIView):
    serializer_class = OptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, question_id, id, *args, **kwargs):
        raise NotImplementedError


class OptionDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def destroy(self, request, id, *args, **kwargs):
        try:
            option = Option.objects.get(id=id)
        except Option.DoesNotExist:
            raise NotFound("Такого варианта ответа не существует")

        if option.question.test.author != request.user:
            raise CantDeleteOptionsForOthersTest

        option_number = option.number

        option.delete()

        options = option.question.options.filter(
            deleted_at__isnull=True, number__gt=option_number
        )

        if options.count() > 0:
            sort_by_number(Option, options, option_number)
        return Response(status=status.HTTP_204_NO_CONTENT)
