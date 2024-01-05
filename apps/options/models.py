from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseModel

from ..questions.models import Question
from ..scales.models import Scale


# Create your models here.
class Option(BaseModel):
    """модель варианта ответа на вопрос"""

    question = models.ForeignKey(
        to=Question,
        related_name="options",
        related_query_name="option",
        verbose_name="Вопрос",
        on_delete=models.CASCADE,
    )

    number = models.PositiveIntegerField(default=1, verbose_name="Номер ответа")

    # поля для вопроса типа range
    min_range = models.IntegerField(
        null=True, blank=True, verbose_name="Минимальный порог"
    )
    max_range = models.IntegerField(
        null=True, blank=True, verbose_name="Максимальный порог"
    )
    # поле для вопроса типа single, multi
    text = models.CharField(
        max_length=255, verbose_name="Текст варианта ответа", blank=True, null=True
    )
    # поле для вопроса типа image
    image = models.ImageField(
        upload_to="test_options",
        blank=True,
        null=True,
        verbose_name="Изображение варианта ответа",
    )

    class Meta:
        verbose_name = "вариант ответа"
        verbose_name_plural = "варианты ответа"
        ordering = ["question", "number", "-created_at"]

    def __str__(self):
        return f"Ответ на {self.question} №{self.number}"


class OptionScore(BaseModel):
    """модель баллов для варианта ответа"""

    option = models.ForeignKey(to=Option, on_delete=models.CASCADE)
    scale = models.ForeignKey(
        to=Scale, on_delete=models.CASCADE, null=True, blank=True
    )  # может быть пустым, при отсутствии шкал

    score = models.SmallIntegerField(verbose_name="Баллы", default=1)

    class Meta:
        verbose_name = "балл варианта ответа"
        verbose_name_plural = "баллы вариантов ответа"
