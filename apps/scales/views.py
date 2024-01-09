from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.scales.models import Scale
from apps.scales.serializers import ScaleSerializer
from apps.tests.models import Test

from .exceptions import (
    CantAddScalesForOthersTests,
    CantDeleteScalesForOthersTests,
    CantUpdateScalesForOthersTests,
    CantViewScalesForOthersTest,
)


# Create your views here.
class TestScalesListAPIView(generics.ListAPIView):
    serializer_class = ScaleSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        test_id = self.kwargs.get("test_id")
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")

        if test.author != self.request.user:
            raise CantViewScalesForOthersTest

        try:
            scales = Scale.objects.filter(test=test, deleted_at__isnull=True)
        except Scale.DoesNotExist:
            raise NotFound("У этого теста нет шкал.")

        return scales


class ScaleCreateAPIView(generics.CreateAPIView):
    serializer_class = ScaleSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, test_id, *args, **kwargs):
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")

        if test.author != request.user:
            raise CantAddScalesForOthersTests

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save(test=test)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ScaleDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def destroy(self, request, test_id, id, *args, **kwargs):
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")

        try:
            scale = Scale.objects.get(id=id)
        except Scale.DoesNotExist:
            raise NotFound("Такой шкалы не существует")

        if test.author != request.user:
            raise CantDeleteScalesForOthersTests

        scale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ScaleUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ScaleSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def patch(self, request, test_id, id, *args, **kwargs):
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            raise NotFound("Такого теста не существует")

        try:
            scale = Scale.objects.get(id=id)
        except Scale.DoesNotExist:
            raise NotFound("Такой шкалы не существует")

        if test.author != request.user:
            raise CantUpdateScalesForOthersTests

        serializer = self.serializer_class(
            instance=scale,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
