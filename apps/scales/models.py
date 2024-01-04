from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseModel

from ..tests.models import Test


# Create your models here.
class Scale(BaseModel):
    name = models.CharField(max_length=125, verbose_name="Scale name")
    description = models.TextField("Description", max_length=255, null=True)
    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        related_name="scales",
        related_query_name="test",
    )

    class Meta:
        verbose_name = "scale"
        verbose_name_plural = "scales"
        ordering = ["-created_at"]
