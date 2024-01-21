from django.contrib.auth import get_user_model
from django.db import models

from apps.base.models import BaseModel
from apps.tests.models import Test

User = get_user_model()


class Notification(BaseModel):
    """Модель уведомлений"""

    class NotificationTypes(models.TextChoices):
        TEST_UNFINISHED = ("unfinished_test", "Не завершенный тест")
        TEST_ASSIGNED = ("assigned_test", "Назначен тест")
        TEST_PUBLISHED = ("published_test", "Тест опубликован")
        # по ходу дела добавлю еще типы

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="notifications",
        related_query_name="notification",
    )

    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        verbose_name="Тест",
        related_name="notifications",
        related_query_name="notification",
    )

    text = models.TextField(max_length=255, verbose_name="Текст уведомления")

    subject = models.CharField(
        choices=NotificationTypes.choices,
        max_length=30,
        verbose_name="Тема уведомления",
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "уведомление"
        verbose_name_plural = "уведомления"
        ordering = ["-created_at"]
