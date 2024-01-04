from django.db import models

from apps.base.models import BaseModel

from ..tests.models import Test


# Create your models here.
class Question(BaseModel):
    """модель вопроса"""

    class QuestionTypes(models.IntegerChoices):
        """содержит типы вопросов"""

        SINGLE_CHOICE = 1, "single"
        MULTI_CHOICE = 2, "multi"
        RANGE = 3, "range"
        OPEN = 4, "open"
        IMAGE = 5, "image"

    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        related_name="questions",
        related_query_name="question",
        verbose_name="Тест",
    )

    type = models.IntegerField(
        choices=QuestionTypes.choices, verbose_name="Тип вопроса"
    )

    text = models.CharField(max_length=255, verbose_name="Текст")

    number = models.PositiveIntegerField(
        verbose_name="Номер вопроса",
        default=1,
    )

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"
        ordering = ["number", "-created_at"]

    def __str__(self):
        return f'Вопрос №{self.number} для теста "{self.test.title}"'


class QuestionImage(BaseModel):
    """модель изображения вопроса"""

    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name="images",
        related_query_name="image",
        verbose_name="Вопрос",
    )

    image = models.ImageField(
        upload_to="question_images",
        verbose_name="Изображение вопроса",
    )

    class Meta:
        verbose_name = "изображение вопроса"
        verbose_name_plural = "изображения вопроса"
        ordering = ["-created_at"]
