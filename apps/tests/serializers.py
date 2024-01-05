from rest_framework import serializers

from ..questions.models import Question
from .models import AssignedTest, Test


class TestSerializer(serializers.ModelSerializer):
    """сериализатор для теста"""

    author = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "author",
            "questions",
        ]

    def get_author(self, obj) -> str:
        # поменять чутка юзера шоб вывести нормально
        return obj.author.email

    def get_questions(self, obj) -> int:
        return obj.questions.count()


class TestCreateUpdateSerializer(serializers.ModelSerializer):
    """сериализатор для создания теста"""

    class Meta:
        model = Test
        fields = [
            "title",
            "description",
        ]
