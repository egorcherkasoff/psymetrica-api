from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _

from .models import AssignedTest, Test


# Register your models here.
class AdminTest(ModelAdmin):
    ordering = ["pkid"]
    model = Test
    fieldsets = (
        (
            _("Основная информация"),
            {"fields": ("title", "description", "author")},
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
                "fields": ("title", "description"),
            },
        ),
    )
    search_fields = ["title", "description"]
    list_filter = ["author"]
    list_display = ["id", "title", "author", "slug"]
    readonly_fields = ["created_at", "updated_at"]


admin.site.register(Test, AdminTest)
admin.site.register(AssignedTest)
