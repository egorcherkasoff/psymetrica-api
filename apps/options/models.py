from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseModel

from ..questions.models import Question
from ..scales.models import Scale


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

    class Meta:
        verbose_name = "вариант ответа"
        verbose_name_plural = "варианты ответа"
        ordering = ["question", "number", "-created_at"]
        unique_together = ["question", "number"]

    def __str__(self):
        return f"Ответ на {self.question} №{self.number}"

    def get_score(self):
        return self.scores.first().score if self.scores.exists() else None

    def get_scale(self):
        return self.scores.first().scale if self.scores.exists() else None


class TextOption(BaseModel):
    """модель варианта ответа на вопрос типа text"""

    option = models.ForeignKey(
        to=Option,
        on_delete=models.CASCADE,
        related_name="text_option",
        verbose_name="Вариант ответа",
    )

    text = models.CharField(max_length=255, verbose_name="Текст варианта ответа")

    class Meta:
        verbose_name = "текстовый вариант ответа"
        verbose_name_plural = "текстовые варианты ответа"

    def __str__(self):
        return self.text


class ImageOption(BaseModel):
    """модель варианта ответа на вопрос типа image"""

    option = models.ForeignKey(
        to=Option,
        on_delete=models.CASCADE,
        related_name="image_option",
        verbose_name="Вариант ответа",
    )

    image = models.ImageField(
        upload_to="test_options",
        verbose_name="Изображение варианта ответа",
    )

    class Meta:
        verbose_name = "вариант ответа с картинкой"
        verbose_name_plural = "варианты ответа с картинкой"

    def __str__(self):
        return self.text


class RangeOption(BaseModel):
    """модель варианта ответа на вопрос типа range"""

    option = models.ForeignKey(
        to=Option,
        on_delete=models.CASCADE,
        related_name="range_option",
        verbose_name="Вариант ответа",
    )

    min_range = models.IntegerField(verbose_name="Минимальный порог")
    max_range = models.IntegerField(verbose_name="Максимальный порог")

    class Meta:
        verbose_name = "вариант ответа с картинкой"
        verbose_name_plural = "варианты ответа с картинкой"

    def __str__(self):
        return self.text


class OptionScore(BaseModel):
    """модель баллов для варианта ответа"""

    option = models.ForeignKey(
        to=Option, on_delete=models.CASCADE, related_name="scores"
    )
    scale = models.ForeignKey(
        to=Scale, on_delete=models.CASCADE, null=True, blank=True
    )  # может быть пустым, при отсутствии шкал

    score = models.SmallIntegerField(verbose_name="Баллы", default=1)

    class Meta:
        verbose_name = "балл варианта ответа"
        verbose_name_plural = "баллы вариантов ответа"

    def __str__(self):
        return f"{self.option} => {self.score} балла по шкале {self.scale}"
