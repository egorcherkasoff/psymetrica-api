import uuid

from django.db import models
from django.utils import timezone

from apps.base.models import BaseModel

from ..questions.models import Question
from ..scales.models import Scale


def filename_to_uuid(instance, filename):
    """генерация уникального имени файла"""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"options/{filename}"


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

    def delete(self):
        """удаление варианта ответа, связанных с ним под-типами и баллами"""
        # удаляем text подтип
        if self.text_option.first():
            self.text_option.first().delete()
        # удаляем range подтип
        if self.range_option.first():
            self.range_option.first().delete()
        # удаляем image подтип
        if self.image_option.first():
            self.image_option.first().delete()

        # удаляем баллы
        if self.scores.first():
            self.scores.first().delete()
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])


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
        upload_to=filename_to_uuid,
        verbose_name="Изображение варианта ответа",
    )

    class Meta:
        verbose_name = "вариант ответа с картинкой"
        verbose_name_plural = "варианты ответа с картинкой"

    def __str__(self):
        return f"{self.option} с картинкой"


class RangeOption(BaseModel):
    """модель варианта ответа на вопрос типа range"""

    option = models.ForeignKey(
        to=Option,
        on_delete=models.CASCADE,
        related_name="range_option",
        verbose_name="Вариант ответа",
    )
    # было бы range на value переименовать )
    min_range = models.IntegerField(verbose_name="Минимальный порог")
    max_range = models.IntegerField(verbose_name="Максимальный порог")

    class Meta:
        verbose_name = "вариант ответа с картинкой"
        verbose_name_plural = "варианты ответа с картинкой"

    def __str__(self):
        return f"{self.option} от {self.min_range} до {self.max_range}"


class OptionScore(BaseModel):
    """модель баллов для варианта ответа"""

    option = models.ForeignKey(
        to=Option,
        on_delete=models.CASCADE,
        related_name="scores",
        verbose_name="Вариант ответа",
    )
    scale = models.ForeignKey(
        to=Scale, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Шкала"
    )  # может быть пустым, при отсутствии шкал

    score = models.SmallIntegerField(verbose_name="Баллы", default=1)

    class Meta:
        verbose_name = "балл варианта ответа"
        verbose_name_plural = "баллы вариантов ответа"

    def __str__(self):
        return f"{self.option} => {self.score} балла по шкале {self.scale}"
