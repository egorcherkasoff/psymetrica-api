from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models

from apps.base.models import BaseModel

User = get_user_model()


# Create your models here.
class Test(BaseModel):
    """Модель теста"""

    name = models.CharField(max_length=155, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="tests",
        related_query_name="user",
    )
    slug = AutoSlugField(
        always_update=True,
        populate_from="name",
        unique=True,
    )

    class Meta:
        verbose_name = "тест"
        verbose_name_plural = "тесты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
