import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from ..questions.models import Question
from ..scales.models import Scale
from ..tests.models import Test


# Create your models here.
class Answer(models.Model):
    # general info
    pkid = models.BigAutoField(editable=False, primary_key=True)
    id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    text = models.CharField(
        max_length=125,
        verbose_name=_("Answer Text"),
    )
    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name="answers",
        related_query_name="question",
        verbose_name=_("Question"),
    )
    scale = models.ForeignKey(
        to=Scale,
        on_delete=models.CASCADE,
        # related_name="answers",
        # related_query_name="scale",
        verbose_name=_("Scale"),
        null=True,
        blank=True,
    )
    number = models.IntegerField(_("Answer Number"), default=1, blank=True)
    points = models.IntegerField(verbose_name=_("Answer points"), default=1, blank=True)
    # timestamps
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("create timestamp")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("update timestamp"))
    deleted_at = models.DateTimeField(
        null=True, default=None, verbose_name=_("delete timestamp"), blank=True
    )

    class Meta:
        verbose_name = _("answer")
        verbose_name_plural = _("answers")
        ordering = ["number", "-created_at"]

    def __str__(self):
        return f"{self.question.test.name}'s question #{self.number}"
