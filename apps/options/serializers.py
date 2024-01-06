from rest_framework import serializers

from .models import Option


class OptionSerializer(serializers.ModelSerializer):
    """сериализатор для вариантов ответа"""

    image = serializers.SerializerMethodField()

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

    def get_image(self, obj):
        try:
            obj.image.url
        except ValueError:
            return None
