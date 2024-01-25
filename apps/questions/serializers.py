from rest_framework import serializers

from apps.tests.serializers import TestDetailSerializer

from ..options.serializers import OptionSerializer
from .models import Question


class QuestionListSerializer(serializers.ModelSerializer):
    """сериализатор для списка вопросов"""

    type = serializers.CharField(source="get_type_display")
    options = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            "id",
            "test",
            "text",
            "image",
            "is_required",
            "options",
        ]

    def get_options(self, obj):
        return obj.options_count

    def get_image(self, obj):
        return obj.get_image()


class QuestionDetailSerializer(QuestionListSerializer):
    """сериализатор отображения одного вопроса"""

    type = serializers.CharField(source="get_type_display")
    options = OptionSerializer(many=True)
    image = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            "id",
            "test",
            "type",
            "text",
            "image",
            "is_required",
            "options",
            "created_at",
        ]

    def get_options(self, obj):
        options = obj.get_options()
        serializer = OptionSerializer(options, many=True)
        return serializer.data

    def get_created_at(self, obj) -> str:
        return obj.get_created_at()


class QuestionCreateSerializer(serializers.ModelSerializer):
    """сериализатор создания вопроса"""

    test_id = serializers.UUIDField(write_only=True, source="test.id")
    test = TestDetailSerializer(many=False, required=False, read_only=True)
    image = serializers.ImageField(required=False)
    type = serializers.CharField()
    created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "test_id",
            "test",
            "number",
            "type",
            "text",
            "image",
            "is_required",
            "created_at",
        ]

    def get_created_at(self, obj):
        return obj.get_created_at()

    def get_type(self, obj):
        return obj.get_type_display()


class QuestionUpdateSerializer(serializers.ModelSerializer):
    """сериализатор обновления вопроса"""

    class Meta:
        model = Question
        fields = ["number", "text", "type", "image", "is_required"]


class QuestionUpdateSerializer(serializers.ModelSerializer):
    """сериализатор изменения вопроса"""

    test = TestDetailSerializer(read_only=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Question
        fields = ["test", "number", "type", "text", "image", "is_required"]


class QuestionUpdateSerializer(serializers.ModelSerializer):
    """сериализатор обновления вопроса"""

    class Meta:
        model = Question
        fields = ["number", "text", "type", "image", "is_required"]
