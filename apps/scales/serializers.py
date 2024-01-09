from rest_framework import serializers
from .models import Scale


class ScaleSerializer(serializers.ModelSerializer):
    test = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Scale
        fields = ["test", "title", "description"]

    def get_test(self, obj):
        return obj.test.title
