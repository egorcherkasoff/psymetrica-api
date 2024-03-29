from colorfield.fields import ColorField
from django.db import models

from apps.base.models import BaseModel

from ..tests.models import Test


class Scale(BaseModel):
    """Модель шкалы"""

    title = models.CharField(max_length=125, verbose_name="Название")
    description = models.TextField("Описание", max_length=255, null=True)
    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        related_name="scales",
        related_query_name="scale",
        verbose_name="Тест",
    )
    color = ColorField(
        default="#ff0000", format="hex", verbose_name="Цвет шкалы в графиках"
    )

    class Meta:
        verbose_name = "шкала"
        verbose_name_plural = "шкалы"
        ordering = ["test", "-created_at"]

    def __str__(self):
        return self.title
