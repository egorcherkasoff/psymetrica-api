from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Question


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    ordering = ["pkid"]
    model = Question
    fieldsets = (
        (
            "Основная информация",
            {"fields": ("test", "number", "type", "text", "image", "is_required")},
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
                "fields": ("test", "number", "type", "text", "image", "is_required"),
            },
        ),
    )
    search_fields = [
        "test__title",
        "text",
        "type",
    ]
    list_filter = ["is_required", "type"]
    list_display = ["id", "test", "number", "type"]
    list_display_links = ["id", "test"]
    readonly_fields = ["created_at", "updated_at"]
    empty_value_display = "-информация отсутствует-"


# @admin.register(QuestionGroup)
# class QuestionGroupAdmin(ModelAdmin):
#     model = QuestionGroup
#     ordering = ["pkid"]
#     fieldsets = (
#         (
#             "Основная информация",
#             {"fields": ("test", "title", "questions")},
#         ),
#         (
#             "Даты",
#             {"fields": ("created_at", "updated_at", "deleted_at")},
#         ),
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("test", "title", "questions"),
#             },
#         ),
#     )
#     search_fields = [
#         "test__title",
#     ]
#     list_display = ["id", "test", "title"]
#     list_display_links = ["id", "test"]
#     readonly_fields = ["created_at", "updated_at"]
#     empty_value_display = "-информация отсутствует-"
