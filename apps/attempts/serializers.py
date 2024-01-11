from rest_framework import serializers

from apps.scales.serializers import ScaleSerializer

from .models import Attempt, AttemptAnswer


class AttemptSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField(read_only=True)
    finished = serializers.SerializerMethodField(read_only=True)
    started = serializers.SerializerMethodField(read_only=True)
    test = serializers.UUIDField(source="test.id", read_only=True)
    user = serializers.UUIDField(source="test.author.id", read_only=True)

    class Meta:
        model = Attempt
        fields = [
            "id",
            "test",
            "user",
            "finished",
            "started",
            "answers",
        ]

    def get_answers(self, obj):
        return AttemptAnswerSerializer(obj.answers.all(), many=True).data

    def get_finished(self, obj):
        return obj.get_finished_date()

    def get_started(self, obj):
        return obj.get_start_date()


class AttemptAnswerSerializer(serializers.ModelSerializer):
    option = serializers.UUIDField(source="option.id")
    score = serializers.IntegerField(read_only=True)
    scale = ScaleSerializer(read_only=True)

    class Meta:
        model = AttemptAnswer
        fields = ["id", "option", "answer", "score", "scale"]


# class AttemptResultsSerialzer(serializers.ModelSerializer):
#     started = serializers.SerializerMethodField(read_only=True)
#     finished = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Attempt
#         fields = [
#             "id",
#             "started",
#             "finished",
#             "test",
#             "user",
#         ]

#     def get_started(self, obj):
#         return obj.get_start_date()

#     def get_finished(self, obj):
#         return obj.get_finished_date()
