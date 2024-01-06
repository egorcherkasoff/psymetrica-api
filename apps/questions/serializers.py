from rest_framework import serializers

from ..options.serializers import OptionSerializer
from ..tests.models import Test
from .models import Question, QuestionImage
from django.core.exceptions import ValidationError
from PIL import Image


class QuestionSerializer(serializers.ModelSerializer):
    """сериализатор отображения вопроса"""

    image = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            "id",
            "number",
            "type",
            "text",
            "image",
            "options",
        ]

    def get_type(self, obj):
        return obj.get_type_display()

    def get_image(self, obj):
        try:
            return obj.images.get(deleted_at__isnull=True).image.url
        except QuestionImage.DoesNotExist:
            return None

    def get_options(self, obj):
        options = obj.options.all()
        serializer = OptionSerializer(options, many=True)
        return serializer.data


class QuestionCreateUpdateSerializer(serializers.ModelSerializer):
    """сериализатор создания и обновления вопроса"""

    image = serializers.ImageField(required=False)

    class Meta:
        model = Question
        fields = ["number", "text", "type", "image"]
