from rest_framework import serializers

from apps.tests.serializers import TestDetailSerializer

from ..options.serializers import OptionSerializer
from .models import Question


class QuestionListSerializer(serializers.ModelSerializer):
    """сериализатор для списка вопросов"""

    options = serializers.IntegerField(source="options_count")
    image = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            "id",
            "type",
            "text",
            "image",
            "is_required",
            "options",
        ]

    def get_image(self, obj):
        return obj.get_image()

    def get_type(self, obj):
        return obj.get_type_display()


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


# TODO: сделать валидацию по полю image тут и в update, и еще number. разобраться почему required false по дефолту...
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
    """сериализатор изменения вопроса"""

    test = TestDetailSerializer(many=False, required=False, read_only=True)
    image = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "test",
            "number",
            "type",
            "text",
            "image",
            "is_required",
            "updated_at",
        ]

    def get_updated_at(self, obj):
        return obj.get_updated_at()

    def get_type(self, obj):
        return obj.get_type_display()

    def get_image(self, obj):
        return obj.image.url if obj.image else None
