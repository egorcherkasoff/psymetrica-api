from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .exceptions import CantAssignTests, CantAssignTestsForYourself, NotYourTest
from .models import Test
from .renderers import TestJSONRenderer, TestsJSONRenderer
from .serializers import TestSerializer, UpdateTestSerializer

User = get_user_model()


# @api_view(["GET"])
# @permission_classes((permissions.AllowAny))
# def get_all_tests(request):
#     tests = Test.objects.filter(deleted_at__isnull=False)
#     serializer = TestSerializer(tests, many=True)
#     namespaced_response = {"tests": serializer.data}
#     return Response(namespaced_response, status=status.HTTP_200_OK)


# @api_view(["GET"])
# @permission_classes((permissions.AllowAny))
# def get_test_details(request, slug):
#     try:
#         test = Test.objects.get(slug=slug)
#     except Test.DoesNotExist:
#         raise NotFound("Test with following url doesnt exist.")

#     serializer = TestSerializer(test, many=False)
#     formatted_response = {"test": serializer.data}
#     return Response(formatted_response, status=status.HTTP_200_OK)


class TestListAPIView(generics.ListAPIView):
    serializer_class = TestSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Test.objects.filter(deleted_at__isnull=False)
    renderer_classes = (TestJSONRenderer,)


class TestDetailAPIView(generics.RetrieveAPIView):
    serializer_class = TestSerializer
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (TestJSONRenderer,)

    def retrieve(self, request, slug, *args, **kwargs):
        try:
            test = Test.objects.get(slug="test")
        except Test.DoesNotExist:
            raise NotFound("Test with following url doesnt exist.")
        serializer = self.serializer_class(test, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateTestAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (TestJSONRenderer,)
    serializer_class = UpdateTestSerializer

    def patch(self, request, slug):
        try:
            test = Test.objects.get(slug=slug)
        except Test.DoesNotExist:
            raise NotFound("Test with following url doesnt exist.")

        user = request.user
        if test.author != user:
            raise NotYourTest

        data = request.data
        serializer = UpdateTestSerializer(instance=test, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
