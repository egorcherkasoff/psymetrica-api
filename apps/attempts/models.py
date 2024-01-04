import uuid

from django.contrib.auth import get_user_model
from django.db import models

from apps.base.models import BaseModel

from ..options.models import Option
from ..tests.models import Test

User = get_user_model()


# Create your models here.
class Attempt(BaseModel):
    """Модель попытки теста"""

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="attempts",
        related_query_name="attempt",
    )

    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        verbose_name="Тест",
        related_name="attempts",
        related_query_name="attempt",
    )

    finished = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата завершения"
    )

    class Meta:
        verbose_name = "попытка"
        verbose_name_plural = "попытки"
        ordering = ["-created_at"]


class AttemptAnswers(BaseModel):
    attempt = models.ForeignKey(
        to=Attempt,
        on_delete=models.CASCADE,
        related_name="answers",
        related_query_name="answer",
    )

    option = models.ForeignKey(
        to=Option,
        on_delete=models.CASCADE,
        related_name="answers",
        related_query_name="answer",
    )

    # поле заполняется только при типе вопроса OPEN или SCALE
    answer = models.CharField(
        max_length=255, verbose_name="Ответ", blank=True, null=True
    )

    class Meta:
        verbose_name = "ответ попытки"
        verbose_name_plural = "ответы попытки"
        ordering = ["-attempt", "-created_at"]
