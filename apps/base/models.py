import uuid

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """абстрактная модель с необходимыми тайстампами и id"""

    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    deleted_at = models.DateTimeField(
        null=True, default=None, verbose_name="Дата удаления", blank=True
    )

    class Meta:
        abstract = True

    def delete(self):
        """совершает 'мягкое' удаление объекта, устанавливая дату удаления"""
        self.deleted_at = timezone.now()
        self.save(update_fields=("deleted_at"))
