from rest_framework import serializers

from apps.scales.serializers import ScaleSerializer

from ..questions.models import Question
from .models import AssignedTest, Test


class TestListSerializer(serializers.ModelSerializer):
    """сериализатор для списка тестов"""

    author = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = [
            "title",
            "author",
            "description",
            "category",
            "slug",
            "questions",
            "created_at",
        ]

    def get_author(self, obj) -> str:
        # поменять чутка юзера шоб вывести нормально
        return obj.author.email

    def get_questions(self, obj) -> int:
        return obj.actual_question_count

    def get_created_at(self, obj) -> str:
        return obj.get_created_at()


class TestDetailSerializer(TestListSerializer):
    """сериализатор для теста"""

    scales = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = [
            "title",
            "author",
            "description",
            "category",
            "slug",
            "questions",
            "created_at",
            "scales",
        ]

    def get_scales(self, obj):
        scales = obj.get_scales()
        serializer = ScaleSerializer(scales, many=True)
        return serializer.data


class TestCreateUpdateSerializer(serializers.ModelSerializer):
    """сериализатор для создания теста"""

    category = serializers.UUIDField(source="category.id", required=False)

    class Meta:
        model = Test
        fields = ["title", "description", "category"]
