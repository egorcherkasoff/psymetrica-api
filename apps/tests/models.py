from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models

from apps.base.models import BaseModel

User = get_user_model()


# Create your models here.
class Test(BaseModel):
    """Модель теста"""

    title = models.CharField(db_index=True, max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="tests",
        related_query_name="test",
        verbose_name="Автор",
    )

    slug = AutoSlugField(
        always_update=True,
        populate_from="title",
        unique=True,
    )

    class Meta:
        verbose_name = "тест"
        verbose_name_plural = "тесты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class AssignedTest(BaseModel):
    """Модель назначения теста"""

    assigned_to = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Кому назначено",
        related_name="assigned_to_tests",
    )
    assigned_by = models.ForeignKey(
        related_name="assigned_by_tests",
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Кто назначил",
    )

    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        verbose_name="Тест",
        related_name="assignments",
    )

    class Meta:
        verbose_name = "Назначение теста"
        verbose_name_plural = "Назначения теста"
        ordering = ["assigned_to", "test", "-created_at"]
