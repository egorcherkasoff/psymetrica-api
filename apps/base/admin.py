from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


# Register your models here.
class AdminGroup(ModelAdmin):
    ordering = ["id"]
    model = Group
    fieldsets = (
        (
            _("general information"),
            {"fields": ("name",)},
        ),
        (_("permissions"), {"fields": ["permissions"]}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide"),
                "fields": ("name", "permissions"),
            },
        ),
    )
    search_fields = ["name"]
    list_filter = ["permissions"]
    list_display = ["id", "name"]


# to change admin display for groups
admin.site.unregister(Group)
admin.site.register(Group, AdminGroup)
