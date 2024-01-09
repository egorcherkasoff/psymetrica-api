from rest_framework import serializers

from apps.questions.models import Question

from .exceptions import IncorrectOptionType
from .models import Option, OptionScore


class OptionSerializer(serializers.ModelSerializer):
    """сериализатор для вариантов ответа"""

    image = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    scale = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = [
            "id",
            "number",
            "min_range",
            "max_range",
            "image",
            "text",
            "score",
            "scale",
        ]

    def get_score(self, obj):
        try:
            score_obj = obj.scores.get()
        except OptionScore.DoesNotExist:
            return None
        return score_obj.score

    def get_scale(self, obj):
        try:
            score_obj = obj.scores.get()
        except OptionScore.DoesNotExist:
            return None
        return score_obj.scale

    def get_image(self, obj):
        try:
            obj.image.url
        except ValueError:
            return None


class OptionCreateUpdateSerializer(serializers.ModelSerializer):
    """сериализатор для создания и обновления варианта ответа"""

    scale = serializers.UUIDField(required=False)
    score = serializers.IntegerField(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Option
        fields = [
            "number",
            "min_range",
            "max_range",
            "image",
            "text",
            "scale",
            "score",
        ]

    def validate(self, attrs):
        """валидация типа ответа в зависимости от типа вопроса"""
        question_id = self.context.get("question_id")
        # обновляем или создаем
        update = self.context.get("update")
        question = Question.objects.get(id=question_id)
        type = question.type
        # у вопроса типа single и multi должно быть поле text
        if type == 1 or type == 2:
            if not update:
                if not attrs.get("text"):
                    raise IncorrectOptionType
            attrs["image"] = None
            attrs["min_range"] = None
            attrs["max_range"] = None
        # у вопроса типа range только min и max range
        elif type == 3:
            if not update:
                if not attrs.get("min_range") or not attrs.get("max_range"):
                    raise IncorrectOptionType
            attrs["text"] = None
            attrs["image"] = None
        # у типа open все поля пустые
        elif type == 4:
            attrs["text"] = None
            attrs["min_range"] = None
            attrs["max_range"] = None
            attrs["image"] = None
        # у типа image должно быть поле image
        else:
            attrs["text"] = None
            attrs["min_range"] = None
            attrs["max_range"] = None
        return attrs
