from django.contrib import admin
from .models import Attempt, AttemptAnswers

# Register your models here.
admin.site.register(Attempt)
admin.site.register(AttemptAnswers)
