from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Attempt, AttemptAnswer


class AttemptAdmin(ModelAdmin):
    list_display = ["id", "test", "user", "finished"]


# Register your models here.
admin.site.register(Attempt, AttemptAdmin)
admin.site.register(AttemptAnswer)
