from django.contrib import admin
from django.contrib.admin import ModelAdmin


from .models import Question, QuestionImage


class QuestionAdmin(ModelAdmin):
    model = Question
    list_display = ["id", "number", "text", "type", "test"]


# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionImage)
