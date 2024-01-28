from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline

from .models import Attempt, AttemptAnswer


class AttemptAnswerInline(StackedInline):
    model = AttemptAnswer
    extra = 0
    verbose_name = "Ответ на попытку"
    verbose_name_plural = "Ответы на попытку"
    min_num = 0


@admin.register(Attempt)
class AttemptAdmin(ModelAdmin):
    model = Attempt
    ordering = ["pkid"]
    fieldsets = (
        (
            "Основная информация",
            {"fields": ("user", "test", "finished")},
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
                "fields": (
                    "test",
                    "user",
                ),
            },
        ),
    )
    inlines = (AttemptAnswerInline,)
    search_fields = ["test__title"]
    list_display = ["id", "test", "user"]
    list_display_links = ["id", "test", "user"]
    readonly_fields = ["finished", "created_at", "updated_at"]
    empty_value_display = "-информация отсутствует-"
