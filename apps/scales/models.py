from django.db import models
from django.utils.translation import gettext_lazy as _

from ..tests.models import Test


# Create your models here.
class Scale(models.Model):
    # general info
    name = models.CharField(max_length=125, verbose_name=_("Scale name"))
    description = models.TextField(_("Description"), max_length=255, null=True)
    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        related_name="scales",
        related_query_name="test",
    )
    # timestamps
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("create timestamp")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("update timestamp"))
    deleted_at = models.DateTimeField(
        null=True, default=None, verbose_name=_("delete timestamp"), blank=True
    )

    class Meta:
        verbose_name = _("scale")
        verbose_name_plural = _("scales")
        ordering = ["-created_at"]
