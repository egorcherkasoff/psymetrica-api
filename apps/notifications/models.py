from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.base.models import BaseModel

User = get_user_model()


class Notification(BaseModel):
    """Модель уведомлений"""

    class NotificationTypes(models.TextChoices):
        TEST_ASSIGNED = ("assigned_test", "Назначен тест")
        TEST_PUBLISHED = ("published_test", "Тест опубликован")
        TEST_DECLINED = ("declined_test", "Тест отклонен")
        # по ходу дела добавлю еще типы

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="notifications",
        related_query_name="notification",
    )

    subject = models.CharField(
        choices=NotificationTypes.choices,
        max_length=15,
        verbose_name="Тема уведомления",
    )

    text = models.TextField(
        max_length=255,
        verbose_name="Текст уведомления",
    )

    # с помощью contenttypes делаем ссылку на объект разных моделей
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "уведомление"
        verbose_name_plural = "уведомления"
        ordering = ["-created_at"]
