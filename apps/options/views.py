from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.questions.models import Question
from apps.questions.permissions import IsQuestionTestAuthor

from .exceptions import (
    CantAddOptionsForOthersTest,
    CantDeleteOptionsForOthersTest,
    CantUpdateOptionsForOthersTest,
    IncorrectOptionNumber,
    OptionTypeOpenMustBeUnique,
    OptionWithNumberExists,
)
from .models import Option, OptionScore
from .serializers import (
    OptionCreateSerializer,
    OptionListSerializer,
    OptionUpdateSerializer,
)


def check_option_number(question, number, create=True):
    """проверяет правильность введенного номера вопроса"""
    number = number
    if create:
        if number > question.options.count() + 1:
            raise IncorrectOptionNumber
    else:
        if number > question.options.count():
            raise IncorrectOptionNumber


class OptionCreate(generics.CreateAPIView):
    """эндпоинт для создания варианта ответа"""

    permission_classes = [
        permissions.IsAuthenticated,
        IsQuestionTestAuthor,
    ]
    serializer_class = OptionCreateSerializer
    parser_classes = [
        MultiPartParser,
    ]

    def get_object(self, id):
        try:
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            raise NotFound("Такого вопроса не существует")
        self.check_object_permissions(self.request, question.test)
        return question

    def post(self, request, *args, **kwargs):
        id = request.data.get("question_id")
        question = self.get_object(id)
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(question=question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OptionUpdate(generics.UpdateAPIView):
    """эндпоинт для удаления варианта овтета"""

    permission_classes = [
        permissions.IsAuthenticated,
        IsQuestionTestAuthor,
    ]
    serializer_class = OptionUpdateSerializer
    parser_classes = [
        MultiPartParser,
    ]

    def get_object(self, id):
        try:
            option = Option.objects.get(id=id)
        except Option.DoesNotExist:
            raise NotFound("Такого варианта ответа не существует")
        self.check_object_permissions(self.request, option.question.test)
        return option

    def update(self, request, id, *args, **kwargs):
        option = self.get_object(id)
        serializer = self.serializer_class(
            instance=option,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class OptionDelete(generics.DestroyAPIView):
    """эндпоинт для удаления варианта овтета"""

    permission_classes = [
        permissions.IsAuthenticated,
        IsQuestionTestAuthor,
    ]

    def get_object(self, id):
        try:
            option = Option.objects.get(id=id)
        except Option.DoesNotExist:
            raise NotFound("Такого варианта ответа не существует")
        self.check_object_permissions(self.request, option.question.test)
        return option

    def delete(self, request, id, *args, **kwargs):
        option = self.get_object(id)
        option.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
