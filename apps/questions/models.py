from django.db import models
from django.utils.translation import gettext_lazy as _

from ..scales.models import Scale
from ..tests.models import Test


# Create your models here.
class Question(models.Model):
    # general info
    text = models.CharField(max_length=125, verbose_name=_(" name"))
    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        related_name="questions",
        related_query_name="test",
        verbose_name=_("Test"),
    )
    number = models.IntegerField(verbose_name=_("Question number"), default=1)
    scale = models.ForeignKey(
        to=Scale,
        on_delete=models.CASCADE,
        related_name="questions",
        related_query_name="scale",
        verbose_name=_("Scale"),
        null=True,
        blank=True,
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
        verbose_name = _("question")
        verbose_name_plural = _("questions")
        ordering = ["-created_at"]
