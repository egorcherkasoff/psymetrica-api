from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from ..tests.models import Test
from .models import Question
from .permissions import IsQuestionTestAuthor
from .serializers import (
    QuestionCreateSerializer,
    QuestionDetailSerializer,
    QuestionUpdateSerializer,
)

User = get_user_model()


class QuestionCreate(generics.CreateAPIView):
    """Эндпоинт для создания вопроса"""

    permission_classes = [
        permissions.IsAuthenticated,
        IsQuestionTestAuthor,
    ]
    serializer_class = QuestionCreateSerializer
    parser_classes = (MultiPartParser,)

    def get_object(self, test_id):
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")
        self.check_object_permissions(self.request, test)
        return test

    def post(self, request, *args, **kwargs):
        test_id = request.data.get("test_id")
        test = self.get_object(test_id)
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(test=test)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class QuestionUpdate(generics.UpdateAPIView):
    """Эндпоинт для обновления вопроса"""

    permission_classes = [
        permissions.IsAuthenticated,
        IsQuestionTestAuthor,
    ]
    serializer_class = QuestionUpdateSerializer
    parser_classes = (MultiPartParser,)

    def get_object(self, id):
        try:
            question = Question.objects.get(id=id, deleted_at__isnull=True)
        except Question.DoesNotExist:
            raise NotFound("Такого вопроса не существует")
        self.check_object_permissions(self.request, question.test)
        return question

    def patch(self, request, id, *args, **kwargs):
        question = self.get_object(id)

        serializer = self.serializer_class(
            instance=question,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionDelete(generics.DestroyAPIView):
    """Эндпоинт для удаления вопроса"""

    permission_classes = [
        permissions.IsAuthenticated,
        IsQuestionTestAuthor,
    ]

    def get_object(self):
        try:
            question = Question.objects.get(id=self.kwargs["id"])
        except Question.DoesNotExist:
            raise NotFound("Такого вопроса не существует")
        self.check_object_permissions(self.request, question.test)
        return question

    def destroy(self, request, id, *args, **kwargs):
        question = self.get_object()
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionDetail(generics.RetrieveAPIView):
    """Эндпоинт возвращает вопрос и его варианты ответа"""

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = QuestionDetailSerializer

    def get_object(self):
        try:
            question = Question.objects.get(id=self.kwargs["id"])
        except Question.DoesNotExist:
            raise NotFound("Такого вопроса не существует")
        return question
