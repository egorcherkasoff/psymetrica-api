from django.contrib import admin

from .models import Attempt, AttemptAnswer

# Register your models here.
admin.site.register(Attempt)
admin.site.register(AttemptAnswer)
