from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.base.services import sort_by_number
from apps.questions.models import Question

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
from .models import Option, OptionScore
from .serializers import OptionCreateUpdateSerializer, OptionSerializer


def check_option_number(question, number, create=True):  # 5 => 6
    """проверяет правильность введенного номера вопроса"""
    number = number
    if create:
        if number > question.options.count() + 1:
            raise IncorrectOptionNumber
    else:
        if number > question.options.count():
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
        except (KeyError, AttributeError):
            score = None
        try:
            scale = request.data.pop("scale")
        except (KeyError, AttributeError):
            scale = None

        serializer = self.serializer_class(
            data=request.data,
            context={
                "request": request,
                "question_id": question_id,
            },
        )
        if serializer.is_valid(raise_exception=True):
            option = serializer.save(question=question)
            if score or scale:
                OptionScore.objects.create(option=option, score=score, scale=scale)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class OptionUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OptionCreateUpdateSerializer
    parser_classes = (MultiPartParser,)

    def patch(self, request, question_id, id, *args, **kwargs):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise NotFound("Такого вопроса не существует.")

        try:
            option = question.options.get(id=id)
        except Option.DoesNotExist:
            raise NotFound("Такого варианта ответа не существует.")

        if question.test.author != request.user:
            raise CantUpdateOptionsForOthersTest

        # проверяем добавил ли пользователь разбалловку или шкалу
        try:
            score = request.data.pop("score")
        except (KeyError, AttributeError):
            score = None
        try:
            scale = request.data.pop("scale")
        except (KeyError, AttributeError):
            scale = None

        serializer = self.serializer_class(
            instance=option,
            data=request.data,
            context={
                "request": request,
                "question_id": question_id,
                "update": True,
            },
            partial=True,
        )
        if serializer.is_valid(raise_exception=True):
            new_number = int(request.data.get("number", None))
            number = option.number
            # для подгона номеров других вариантов ответа смотрим, были ли вообще новый номер в запросе
            if new_number:
                # если старый и новый не отличаются, то просто ставим в сериализатор текущее значение
                if new_number != number:
                    # смотрим, чтобы номер был не больше количества вариантов ответа в вопросе
                    check_option_number(question, new_number, False)
                    number = new_number

            serializer.save(number=number)
            options = question.options.exclude(deleted_at__isnull=True)
            sort_by_number(Option, options)
            # подгоняем изменения к остальным номерам если изменился номер этого

            # если пользователь добавил шкалу или баллы к варианту ответа, то смотрим, если было предыдущее значение
            if score or scale:
                try:
                    score_obj = option.scores.first()
                except OptionScore.DoesNotExist:
                    score_obj = None
                # если да - обновляем новыми значениями
                if score_obj:
                    score_obj.score = score
                    score_obj.scale = scale
                    score_obj.save(update_fields=["score", "scale"])
                else:
                    OptionScore.objects.create(option=option, score=score, scale=scale)
            return Response(serializer.data, status=status.HTTP_200_OK)


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
        # если остались другие варианты ответа, то подгоняем номера оставшихся
        if options.count() > 0:
            sort_by_number(Option, options, option_number)
        return Response(status=status.HTTP_204_NO_CONTENT)
