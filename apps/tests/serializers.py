from rest_framework import serializers

from .models import Test


class TestSerializer(serializers.ModelSerializer):
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
        return f"{obj.user.first_name.title} {obj.user.middle_name.title() if obj.user.middle_name else ''} {obj.user.last_name.title()}"


class UpdateTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = [
            "name",
            "description",
        ]
