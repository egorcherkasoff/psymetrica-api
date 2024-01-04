from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.base.models import BaseModel
from ..tests.models import Test


# Create your models here.
class Question(BaseModel):
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

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")
        ordering = ["number", "-created_at"]

    def __str__(self):
        return f"{self.test.name}'s question #{self.number}"
