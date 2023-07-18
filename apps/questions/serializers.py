from rest_framework import serializers

from .models import Question


class QuestionSerializer(serializers.ModelField):
    """сериализатор отображения вопросов"""

    number = serializers.IntegerField()
    name = serializers.CharField()
    test = serializers.CharField(source="test.name")
    # add answers...

    class Meta:
        model = Question
        fields = [
            "number",
            "text",
            "test",
        ]
