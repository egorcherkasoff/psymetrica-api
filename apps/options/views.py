from django.shortcuts import render
from .exceptions import (
    CantAddOptionsForOthersTest,
    CantDeleteOptionsForOthersTest,
    CantUpdateOptionsForOthersTest,
    IncorrectOptionNumber,
    IncorrectOptionType,
    OptionNotForThisQuestion,
    OptionWithNumberExists,
)
from rest_framework import permissions

from .serializers import OptionSerializer
from .models import Question

from rest_framework import generics
from rest_framework.views import APIView


# QuestionOptionListAPIView
class QuestionOptionListAPIView(generics.ListAPIView):
    serializer_class = OptionSerializer
    queryset = Question.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]
