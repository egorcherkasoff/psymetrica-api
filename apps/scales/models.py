from django.db import models

from apps.base.models import BaseModel

from ..tests.models import Test


# Create your models here.
class Scale(BaseModel):
    """Модель шкалы"""

    title = models.CharField(max_length=125, verbose_name="Название")
    description = models.TextField("Описание", max_length=255, null=True)
    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        related_name="scales",
        related_query_name="scale",
    )

    class Meta:
        verbose_name = "шкала"
        verbose_name_plural = "шкалы"
        ordering = ["test", "-created_at"]
