from django.contrib import admin

from .models import Question, QuestionImage

# Register your models here.
admin.site.register(Question)
admin.site.register(QuestionImage)
