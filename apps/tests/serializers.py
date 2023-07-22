from rest_framework import serializers

from ..questions.models import Question
from .models import Test


class TestListSerializer(serializers.ModelSerializer):
    """сериализатор для отображения списка тестов"""

    author = serializers.CharField(source="author.get_full_name")
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = [
            "name",
            "description",
            "author",
            "questions",
        ]

    def get_questions(self, obj):
        return Question.objects.filter(test=obj).count()


class TestDetailSerializer(serializers.ModelSerializer):
    """сериализатор для отображения теста"""

    author = serializers.CharField(source="author.get_full_name")
    questions = serializers.SerializerMethodField()
    # add questions...

    class Meta:
        model = Test
        fields = [
            "name",
            "description",
            "author",
            "questions",
            "created_at",
            "updated_at",
        ]

    def get_questions(self, obj):
        return Question.objects.filter(test=obj).count()


class TestCreateSerializer(serializers.ModelSerializer):
    """сериализатор для создания теста"""

    class Meta:
        model = Test
        fields = [
            "name",
            "description",
        ]


class TestUpdateSerializer(serializers.ModelSerializer):
    """сериализатор для обновления теста"""

    name = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = Test
        fields = [
            "name",
            "description",
        ]
