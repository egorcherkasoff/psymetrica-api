from rest_framework import serializers

from ..options.serializers import OptionSerializer
from ..tests.models import Test
from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    """сериализатор отображения списка вопросов"""

    test = serializers.CharField(source="test.name")
    Options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            "number",
            "text",
            "test",
            "Options",
        ]


class QuestionUpdateSerializer(serializers.ModelSerializer):
    """сериализатор для обновления вопросов"""

    class Meta:
        model = Question
        fields = [
            "text",
        ]


class QuestionCreateSerializer(serializers.ModelSerializer):
    """сериализатор для создания вопросов"""

    test = serializers.SlugRelatedField(
        slug_field="slug", queryset=Test.objects.filter(deleted_at__isnull=True)
    )

    class Meta:
        model = Question
        fields = ["text", "test"]
