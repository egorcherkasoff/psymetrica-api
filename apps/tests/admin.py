from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _

from .models import Test


# Register your models here.
class AdminTest(ModelAdmin):
    ordering = ["id"]
    model = Test
    fieldsets = (
        (
            _("general information"),
            {"fields": ("name", "description", "author")},
        ),
        (
            _("timestamps"),
            {"fields": ("created_at", "updated_at", "deleted_at")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("name", "description"),
            },
        ),
    )
    search_fields = ["name", "description"]
    list_filter = ["author"]
    list_display = ["id", "name", "author", "slug"]
    readonly_fields = ["created_at", "updated_at"]


admin.site.register(Test, AdminTest)
