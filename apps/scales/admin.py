from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Scale


class ScaleAdmin(ModelAdmin):
    list_display = ["id", "title", "description", "test"]


# Register your models here.
admin.site.register(Scale, ScaleAdmin)
