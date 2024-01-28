from rest_framework import serializers

from apps.questions.models import Question
from apps.scales.serializers import ScaleSerializer

from .models import ImageOption, Option, OptionScore, RangeOption, TextOption


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


class OptionScoreSerializer(serializers.ModelSerializer):
    """сериализатор балла варианта ответа"""

    scale = ScaleSerializer()

    class Meta:
        model = OptionScore
        fields = ["score", "scale"]


class OptionListSerializer(serializers.ModelSerializer):
    """сериализатор списка вариантов ответа"""

    body = serializers.SerializerMethodField(
        read_only=True,
    )

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


class OptionCreateSerializer(OptionListSerializer):
    """сериализатор создания варианта ответа"""

    question_id = serializers.UUIDField(source="question.id", write_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    text = serializers.CharField(required=False, write_only=True)
    image = serializers.ImageField(required=False, write_only=True)
    min_range = serializers.IntegerField(required=False, write_only=True)
    max_range = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = Option
        fields = [
            "question_id",
            "id",
            "number",
            "text",
            "image",
            "min_range",
            "max_range",
            "body",
            "created_at",
        ]

    def get_created_at(self, obj):
        return obj.get_created_at()

    def create(self, validated_data):
        """вместе с созданием варианта ответа создаем под-типы option (range, image,text..)"""
        option_data = {
            "question": validated_data["question"],
            "number": validated_data["number"],
        }
        # создаем option, но пока не удостовримся в валидности других полей, сохранять не будем
        option = Option(**option_data)

        if (
            option.question.type == Question.QuestionTypes.SINGLE_OPTION
            or option.question.type == Question.QuestionTypes.MULTIPLE_OPTIONS
        ):
            serializer = TextOptionSeriaizer(data=validated_data)
        elif option.question.type == Question.QuestionTypes.RANGE:
            serializer = RangeOptionSeriaizer(data=validated_data)
            if serializer.is_valid(raise_exception=True):
                option.save()
                serializer.save(option=option)
        elif option.question.type == Question.QuestionTypes.IMAGE:
            serializer = ImageOptionSeriaizer(data=validated_data)
            if serializer.is_valid(raise_exception=True):
                option.save()
                serializer.save(option=option)
        return option


class OptionUpdateSerializer(serializers.ModelSerializer):
    """сериализатор для обновления варианта ответа"""

    text = serializers.CharField(required=False, write_only=True)
    image = serializers.ImageField(required=False, write_only=True)
    min_range = serializers.IntegerField(required=False, write_only=True)
    max_range = serializers.IntegerField(required=False, write_only=True)
    body = serializers.SerializerMethodField(read_only=True, required=False)
    created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Option
        fields = [
            "id",
            "number",
            "text",
            "image",
            "min_range",
            "max_range",
            "body",
            "created_at",
        ]

    def get_created_at(self, obj):
        return obj.get_created_at()

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

    def update(self, instance, validated_data):
        """вместе с вараинтом ответа редачим и под-типы option (range, image,text..)"""
        if "number" in validated_data:
            option_data = {
                "number": validated_data["number"],
            }
            super().update(instance, option_data)

        if (
            instance.question.type == Question.QuestionTypes.SINGLE_OPTION
            or instance.question.type == Question.QuestionTypes.MULTIPLE_OPTIONS
        ):
            serializer = TextOptionSeriaizer(
                instance=instance.text_option.first(), data=validated_data, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                instance.save()
        elif instance.question.type == Question.QuestionTypes.RANGE:
            serializer = RangeOptionSeriaizer(
                instance=instance.range_option.first(),
                data=validated_data,
                partial=True,
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                instance.save()
        elif instance.question.type == Question.QuestionTypes.IMAGE:
            serializer = ImageOptionSeriaizer(
                instance=instance.image_option.first(),
                data=validated_data,
                partial=True,
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                instance.save()
        return instance
