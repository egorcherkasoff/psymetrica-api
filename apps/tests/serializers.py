from rest_framework import serializers

from apps.scales.serializers import ScaleSerializer
from apps.users.serializers import UserSerializer

from .models import AssignedTest, Test, Category


class TestListSerializer(serializers.ModelSerializer):
    """сериализатор для списка тестов"""

    author = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = [
            "id",
            "title",
            "author",
            "description",
            "category",
            "slug",
            "questions",
            "created_at",
        ]

    def get_author(self, obj) -> str:
        # поменять чутка юзера шоб вывести нормально
        return obj.author.email

    def get_questions(self, obj) -> int:
        return obj.actual_question_count

    def get_created_at(self, obj) -> str:
        return obj.get_created_at()

    def get_category(self, obj):
        category = obj.category
        if category:
            return category.title
        return None


class TestDetailSerializer(TestListSerializer):
    """сериализатор для теста"""

    scales = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    created_at = serializers.CharField(read_only=True, source="get_created_at")
    category = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = [
            "title",
            "author",
            "description",
            "category",
            "slug",
            "questions",
            "created_at",
            "scales",
        ]

    def get_scales(self, obj):
        scales = obj.get_scales()
        serializer = ScaleSerializer(scales, many=True)
        return serializer.data

    def get_author(self, obj):
        author = obj.author
        serializer = UserSerializer(author, many=False)
        return serializer.data

    def get_category(self, obj):
        category = obj.category
        serializer = CategorySerializer(category, many=False)
        return serializer.data


class TestCreateSerializer(serializers.ModelSerializer):
    """сериализатор для создания теста"""

    category = serializers.UUIDField(source="category.id", required=False)
    created_at = serializers.CharField(read_only=True, source="get_created_at")

    class Meta:
        model = Test
        fields = ["id", "title", "description", "category", "created_at"]


class TestUpdateSerializer(TestCreateSerializer):
    """сериализатор для обновления теста"""

    category = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ["id", "title", "description", "category", "updated_at"]

    def get_category(self, obj):
        category = obj.category
        serializer = CategorySerializer(category, many=False)
        return serializer.data


class TestAssignSerializer(serializers.ModelSerializer):
    """сериализатор для назначения теста"""

    test = serializers.UUIDField(source="test.id", read_only=True)
    assigned_by = serializers.SerializerMethodField(read_only=True)
    assigned_to = serializers.SerializerMethodField()

    class Meta:
        model = AssignedTest
        fields = ["test", "assigned_to", "assigned_by", "created_at"]

    def get_assigned_by(self, obj):
        assigned_by = obj.assigned_by
        serializer = UserSerializer(assigned_by, many=False)
        return serializer.data

    def get_assigned_to(self, obj):
        assigned_by = obj.assigned_by
        serializer = UserSerializer(assigned_by, many=False)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    """сериализатор для списка категорий"""

    class Meta:
        model = Category
        fields = ["id", "title", "slug"]
