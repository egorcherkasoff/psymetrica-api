from rest_framework import serializers

from apps.questions.models import Question

from .models import Option, OptionScore, ImageOption, RangeOption, TextOption


class ImageOptionSeriaizer(serializers.ModelSerializer):
    """сериализатор варианта ответа с картинкой"""

    image = serializers.SerializerMethodField()

    class Meta:
        model = ImageOption
        fields = ["image"]

    def get_image(self, obj):
        return obj.image.url if obj.image else None


class TextOptionSeriaizer(serializers.ModelSerializer):
    """сериализатор варианта ответа с текстом"""

    class Meta:
        model = TextOption
        fields = ["text"]


class RangeOptionSeriaizer(serializers.ModelSerializer):
    """сериализатор варианта ответа с числовым значением"""

    class Meta:
        model = RangeOption
        fields = ["min_range", "max_range"]


class OptionListSerizlier(serializers.ModelSerializer):
    """сериализатор списка вариантов ответа"""

    body = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = Option
        fields = [
            "id",
            "number",
            "body",
        ]

    def get_body(self, obj):
        if obj.question.type == Question.QuestionTypes.SINGLE_OPTION:
            serializer = TextOptionSeriaizer(obj.text_option.first(), many=False)
            return serializer.data
        elif obj.question.type == Question.QuestionTypes.MULTIPLE_OPTIONS:
            serializer = TextOptionSeriaizer(obj.text_option.first(), many=False)
            return serializer.data
        elif obj.question.type == Question.QuestionTypes.TEXT:
            return None
        elif obj.question.type == Question.QuestionTypes.RANGE:
            serializer = RangeOptionSeriaizer(obj.range_option.first(), many=False)
            return serializer.data
        elif obj.question.type == Question.QuestionTypes.IMAGE:
            serializer = ImageOptionSeriaizer(obj.image_option.first(), many=False)
            return serializer.data
