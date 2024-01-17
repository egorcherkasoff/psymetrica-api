from django.db import models
from apps.base.models import BaseModel
from django.contrib.auth import get_user_model

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
        realated_name="notifications",
        related_query_name="notification",
    )

    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        verbose_name="Тест",
        realated_name="notifications",
        related_query_name="notification",
    )

    text = models.TextField(max_length=255, verbose_name="Текст уведомления")

    subject = models.CharField(choice=NotificationTypes, max_length=255)

    def __str__(self):
        return self.text
