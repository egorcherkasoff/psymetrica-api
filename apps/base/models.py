import uuid

from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    """ абстрактная модель с необходимыми тайстампами и id """
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False)

    #timestamps
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="create timestamp"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="update timestamp")
    deleted_at = models.DateTimeField(
        null=True, default=None, verbose_name="delete timestamp", blank=True
    )

    class Meta:
        abstract = True

    def delete(self):
        """ совершает 'мягкое' удаление объекта, устанавливая дату удаления """
        self.deleted_at = timezone.now()
        self.save(update_fields=("deleted_at"))