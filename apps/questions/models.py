from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseModel

from ..tests.models import Test


# Create your models here.
class Question(BaseModel):
    # general info
    text = models.CharField(max_length=125, verbose_name="Текст")
    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        related_name="questions",
        related_query_name="test",
        verbose_name="Тест",
    )
    # поменять на positiveintfield
    number = models.IntegerField(
        verbose_name="Номер вопроса",
        default=1,
    )

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"
        ordering = ["number", "-created_at"]

    def __str__(self):
        return f'Вопрос номер {self.number} для теста "{self.test.name}"'
