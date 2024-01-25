from rest_framework import serializers

from apps.questions.models import Question

from .exceptions import IncorrectOptionType
from .models import Option, OptionScore


class OptionSerializer(serializers.ModelSerializer):
    """сериализатор для вариантов ответа"""

    score = serializers.SerializerMethodField()
    scale = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = [
            "id",
            "number",
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


class OptionCreateUpdateSerializer(serializers.ModelSerializer):
    """сериализатор для создания и обновления варианта ответа"""

    scale = serializers.UUIDField(required=False)
    score = serializers.IntegerField(required=False)

    class Meta:
        model = Option
        fields = [
            "number",
            "scale",
            "score",
        ]
