from rest_framework import serializers
from apps.options.models import Option

from rest_framework.exceptions import NotFound
from apps.options.serializers import OptionListSerializer
from apps.scales.serializers import ScaleSerializer
from apps.tests.serializers import TestListSerializer
from apps.users.serializers import UserSerializer

from django.core.exceptions import ValidationError
from .models import Attempt, AttemptAnswer


class AnswerSerializer(serializers.ModelSerializer):
    """сериализатор для ответа попытки"""

    option = OptionListSerializer(many=False)
    scale = ScaleSerializer(many=False)

    class Meta:
        model = AttemptAnswer
        fields = [
            "id",
            "option",
            "answer",
            "score",
            "scale",
        ]


class AttemptListSerializer(serializers.ModelSerializer):
    """сериализатор для списка попыток"""

    started_at = serializers.CharField(source="get_start_date")

    class Meta:
        model = Attempt
        fields = [
            "id",
            "test",
            "user",
            "started_at",
            "is_finished",
        ]


class AttemptDetailSerializer(AttemptListSerializer):
    """сериализатор для попытки"""

    answers = serializers.SerializerMethodField()
    finished_at = serializers.CharField(source="get_finish_date")

    class Meta:
        model = Attempt
        fields = [
            "id",
            "test",
            "user",
            "started_at",
            "is_finished",
            "finished_at",
            "answers",
        ]

    def get_answers(self, obj):
        return AnswerSerializer(obj.get_answers(), many=True).data


class AttemptCreateSerializer(AttemptListSerializer):
    """сериализатор для создания попытки"""

    started_at = serializers.CharField(source="get_start_date", read_only=True)
    is_finished = serializers.BooleanField(read_only=True)
    attempt_test = serializers.UUIDField(source="test.id", write_only=True)
    user = UserSerializer(many=False, read_only=True)
    test = TestListSerializer(many=False, read_only=True)

    class Meta:
        model = Attempt
        fields = [
            "id",
            "attempt_test",
            "test",
            "user",
            "started_at",
            "is_finished",
        ]


class AnswerCreateSerializer(serializers.ModelSerializer):
    """сериализатор для добавления ответа"""

    option_id = serializers.UUIDField(write_only=True)
    option = OptionListSerializer(many=False, read_only=True)
    created_at = serializers.CharField(source="get_created_at", read_only=True)

    class Meta:
        model = AttemptAnswer
        fields = ["id", "option_id", "option", "answer", "created_at"]

    def create(self, validated_data):
        # достаем option, чтобы проверить есть ли она
        option_id = validated_data.pop("option_id")
        try:
            option = Option.objects.get(id=option_id, deleted_at__isnull=True)
        except Option.DoesNotExist:
            raise NotFound("Такого варианта ответа не существует")
        validated_data["option"] = option
        # создаем instance для вызова clean метода модели
        self.instance = AttemptAnswer(**validated_data)
        self.instance.clean()
        # если все ок создаем вариант
        return super().create(validated_data)
