from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _

from .models import AssignedTest, Test, Category


@admin.register(Test)
class AdminTest(ModelAdmin):
    ordering = ["pkid"]
    model = Test
    fieldsets = (
        (
            _("Основная информация"),
            {"fields": ("title", "description", "category", "author", "is_published")},
        ),
        (
            _("Даты"),
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
    list_display = ["id", "title", "category", "author", "slug"]
    list_display_links = ["id", "title"]
    readonly_fields = ["created_at", "updated_at"]
    empty_value_display = "-информация отсутствует-"


@admin.register(AssignedTest)
class AdminAssignedTest(ModelAdmin):
    ordering = ["pkid"]
    model = Test
    fieldsets = (
        (
            _("Основная информация"),
            {"fields": ("test", "assigned_to", "assigned_by")},
        ),
        (
            _("Даты"),
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
            _("Основная информация"),
            {"fields": ("title",)},
        ),
        (
            _("Даты"),
            {"fields": ("created_at", "updated_at", "deleted_at")},
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
    readonly_fields = ["created_at", "updated_at"]
    empty_value_display = "-информация отсутствует-"
