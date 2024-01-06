from rest_framework import serializers

from .models import Option


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
        ]

    def get_score(self, obj):
        return obj.scores.first().score

    def get_scale(self, obj):
        return obj.scores.first().scale

    def get_image(self, obj):
        try:
            obj.image.url
        except ValueError:
            return None
