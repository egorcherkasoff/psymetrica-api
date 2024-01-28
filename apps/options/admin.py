from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline

from .models import ImageOption, Option, OptionScore, RangeOption, TextOption


class TextOptionInline(StackedInline):
    model = TextOption
    extra = 0
    verbose_name = "текстовый вариант ответа"
    verbose_name_plural = "текстовые варианты ответа"
    max_num = 1
    min_num = 0


class RangeOptionInline(StackedInline):
    model = RangeOption
    extra = 0
    verbose_name = "вариант ответа с диапазоном"
    verbose_name_plural = "варианты ответа с диапазоном"
    max_num = 1
    min_num = 0


class ImageOptionInline(StackedInline):
    model = ImageOption
    extra = 0
    verbose_name = "вариант ответа с изображением"
    verbose_name_plural = "варианты ответа с изображением"
    max_num = 1
    min_num = 0


class ImageOptionInline(StackedInline):
    model = ImageOption
    extra = 0
    verbose_name = "вариант ответа с изображением"
    verbose_name_plural = "варианты ответа с изображением"
    max_num = 1
    min_num = 0


class OptionScoreInline(StackedInline):
    model = OptionScore
    extra = 0
    verbose_name = "балл варианта ответа"
    verbose_name_plural = "баллы варианта ответа"
    max_num = 1
    min_num = 0


@admin.register(Option)
class OptionAdmin(ModelAdmin):
    model = Option
    ordering = ["pkid"]
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "question",
                    "number",
                )
            },
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
                    "question",
                    "number",
                ),
            },
        ),
    )
    inlines = (
        TextOptionInline,
        RangeOptionInline,
        ImageOptionInline,
        OptionScoreInline,
    )
    search_fields = ["question__text", "question__test__title"]
    list_display = ["id", "question", "number"]
    list_display_links = ["id", "question"]
    readonly_fields = ["created_at", "updated_at"]
    empty_value_display = "-информация отсутствует-"
