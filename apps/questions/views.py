from django.shortcuts import render
from rest_framework import generics, permissions

from ..tests.models import Test
from .exceptions import CantAddQuestionsForOthersTest, QuestionNotForThisTest
from .models import Question
from .pagination import QuestionPagination
from .renderers import QuestionJSONRenderer
from .serializers import QuestionSerializer

# Create your views here.
# class QuestionCreateAPIView(generics.CreateAPIView):
#     renderer_classes = QuestionJSONRenderer
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = QuestionSerializer

#     def create(self, request, *args, **kwargs):
#         test = Test.objects.get(request.data["test"])
#         if serializer.is_valid():
#             serializer.save()
