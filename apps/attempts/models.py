import uuid

from django.contrib.auth import get_user_model
from django.db import models

from apps.base.models import BaseModel

from ..answers.models import Answer
from ..tests.models import Test

User = get_user_model()


# Create your models here.
class Attempt(BaseModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)


# class AttemptAnswers(models.Model):
#     attempt = models.ForeignKey(to=Attempt, on_delete=models.CASCADE)
#     answer = models.ForeignKey(to=Answer, on_delete=models.CASCADE)
#     text = models.TextField(max_length=True, blank=True, null=True)
#     answered_at = models.DateTimeField(auto_now_add=True)
