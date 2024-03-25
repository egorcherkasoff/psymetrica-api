from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import AssignedTest, Category, Test


@admin.register(Test)
class AdminTest(ModelAdmin):
    ordering = ["pkid"]
    model = Test
    fieldsets = (
        (
            "Основная информация",
            {"fields": ("title", "description", "category", "author", "is_published")},
        ),
        (
            "Даты",
            {"fields": ("created_at", "updated_at", "deleted_at")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("title", "description", "is_published"),
            },
        ),
    )
    search_fields = [
        "title",
        "description",
        "category__title",
        "author__first_name",
        "author__last_name",
        "author__middle_name",
    ]
    list_filter = ["author", "is_published"]
    # id только для разработки.. потом убрать
    list_display = [
        "id",
        "title",
        "category",
        "author",
    ]
    list_display_links = ["id", "title"]
    readonly_fields = ["created_at", "updated_at"]
    empty_value_display = "-информация отсутствует-"


@admin.register(AssignedTest)
class AdminAssignedTest(ModelAdmin):
    ordering = ["pkid"]
    model = Test
    fieldsets = (
        (
            "Основная информация",
            {"fields": ("test", "assigned_to", "assigned_by")},
        ),
        (
            "Даты",
            {"fields": ("created_at", "updated_at", "deleted_at")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("test", "assigned_to", "assigned_by"),
            },
        ),
    )
    search_fields = [
        "test__title",
        "assigned_to__first_name",
        "assigned_to__middle_name",
        "assigned_to__last_name",
        "assigned_by__first_name",
        "assigned_by__middle_name",
        "assigned_by__last_name",
    ]
    # TODO: добавить is completed фильтр
    list_filter = []
    # id только для разработки.. потом убрать
    list_display = ["id", "test", "assigned_to", "assigned_by", "created_at"]
    list_display_links = ["id", "test"]
    readonly_fields = ["created_at", "updated_at"]
    empty_value_display = "-информация отсутствует-"


@admin.register(Category)
class AdminCategory(ModelAdmin):
    ordering = ["pkid"]
    model = Test
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": ("title",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("title"),
            },
        ),
    )
    search_fields = [
        "title",
    ]
    list_filter = []
    # id только для разработки.. потом убрать
    list_display = ["id", "title"]
    list_display_links = ["id", "title"]
    empty_value_display = "-информация отсутствует-"
