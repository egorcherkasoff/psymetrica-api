import uuid

from django.db import models
from django.utils import timezone


class SlimModel(models.Model):
    """абстрактная модель с минимальным кол-вом полей, нужна там, где таймстампы и мягкое удаление будут излишни"""

    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseModel(SlimModel):
    """абстрактная модель с более подробными полями. используется там, где нужны таймстампы"""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    deleted_at = models.DateTimeField(
        null=True, default=None, verbose_name="Дата удаления", blank=True
    )

    class Meta:
        abstract = True

    def get_created_at(self):
        return self.created_at.strftime("%d.%m.%Y в %H:%M")

    def get_updated_at(self):
        return self.updated_at.strftime("%d.%m.%Y в %H:%M")

    def delete(self):
        """совершает 'мягкое' удаление объекта, устанавливая дату удаления"""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def hard_delete(self):
        """совершает полное удаление объекта"""
        super().delete()
