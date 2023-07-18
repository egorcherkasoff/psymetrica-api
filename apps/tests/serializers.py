from rest_framework import serializers

from .models import Test


class TestSerializer(serializers.ModelSerializer):
    """сериализатор для отображения теста"""

    name = serializers.CharField()
    description = serializers.CharField()
    author = serializers.SerializerMethodField(read_only=True)
    # add questions...

    class Meta:
        model = Test
        fields = [
            "id",
            "name",
            "description",
            "author",
        ]

    def get_author(self, obj):
        try:
            return f"{obj.author.first_name.title()} {obj.author.middle_name.title() if obj.author.middle_name else ''} {obj.author.last_name.title()}"
        except AttributeError:
            return obj.author.__str__()


class TestUpdateSerializer(serializers.ModelSerializer):
    """сериализатор для обновления теста"""

    name = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = Test
        fields = [
            "name",
            "description",
        ]
