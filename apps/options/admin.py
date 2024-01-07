from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Option, OptionScore


class OptionAdmin(ModelAdmin):
    model = Option
    list_display = [
        "id",
        "question",
        "number",
        "text",
        "min_range",
        "max_range",
        "image",
    ]


# Register your models here.
admin.site.register(Option, OptionAdmin)
admin.site.register(OptionScore)
