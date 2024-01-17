from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Scale


@admin.register(Scale)
class ScaleAdmin(ModelAdmin):
    ordering = ["pkid"]
    model = Scale
    fieldsets = (
        (
            "Основная информация",
            {"fields": ("title", "description", "test", "color")},
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
                "fields": ("title", "description", "test", "color"),
            },
        ),
    )
    search_fields = [
        "title",
        "description",
        "test__title",
    ]
    # TODO: добавить is completed фильтр
    list_filter = []
    # id только для разработки.. потом убрать
    list_display = ["id", "test", "title", "color"]
    list_display_links = ["id", "title"]
    readonly_fields = ["created_at", "updated_at"]
    empty_value_display = "-информация отсутствует-"
