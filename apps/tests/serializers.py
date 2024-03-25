from rest_framework import serializers

from apps.scales.serializers import ScaleSerializer
from apps.users.serializers import UserSerializer

from .models import AssignedTest, Category, Test


class TestListSerializer(serializers.ModelSerializer):
    """сериализатор для списка тестов"""

    author = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    passes = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = [
            "id",
            "title",
            "author",
            "description",
            "category",
            "questions",
            "created_at",
            "passes",
        ]

    def get_author(self, obj):
        author = obj.author
        serializer = UserSerializer(author, many=False)
        return serializer.data

    def get_questions(self, obj) -> int:
        return obj.actual_question_count

    def get_created_at(self, obj) -> str:
        return obj.get_created_at()

    def get_category(self, obj):
        category = obj.category
        if category:
            return category.title
        return None

    def get_passes(self, obj):
        return obj.total_passes


class TestDetailSerializer(TestListSerializer):
    """сериализатор для теста"""

    class Meta:
        model = Test
        fields = [
            "id",
            "title",
            "author",
            "description",
            "category",
            "is_published",
            "show_results_to_user",
            "allow_repeated_attempts",
            "user_can_go_back",
            "created_at",
            "passes",
        ]


class TestCreateSerializer(serializers.ModelSerializer):
    """сериализатор для создания теста"""

    category = serializers.UUIDField(source="category.id", required=False)

    class Meta:
        model = Test
        fields = [
            "title",
            "description",
            "category",
            "show_results_to_user",
            "allow_repeated_attempts",
            "user_can_go_back",
        ]


class TestUpdateSerializer(TestCreateSerializer):
    """сериализатор для обновления теста"""

    category = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = [
            "title",
            "description",
            "category",
            "show_results_to_user",
            "allow_repeated_attempts",
            "user_can_go_back",
        ]

    def get_category(self, obj):
        category = obj.category
        serializer = CategorySerializer(category, many=False)
        return serializer.data


class TestAssignSerializer(serializers.ModelSerializer):
    """сериализатор для назначения теста"""

    assigned_by = serializers.SerializerMethodField(read_only=True)
    assigned_to = serializers.SerializerMethodField()

    class Meta:
        model = AssignedTest
        fields = [
            "assigned_to",
            "assigned_by",
            "created_at",
        ]

    def get_assigned_by(self, obj):
        assigned_by = obj.assigned_by
        serializer = UserSerializer(assigned_by, many=False)
        return serializer.data

    def get_assigned_to(self, obj):
        assigned_by = obj.assigned_by
        serializer = UserSerializer(assigned_by, many=False)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    """сериализатор для категорий"""

    class Meta:
        model = Category
        fields = [
            "id",
            "title",
        ]
