import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseModel

from ..questions.models import Question
from ..scales.models import Scale
from ..tests.models import Test


# Create your models here.
class Answer(BaseModel):
    text = models.CharField(
        max_length=125,
        verbose_name="Answer Text",
    )
    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name="answers",
        related_query_name="question",
        verbose_name="Question",
    )
    scale = models.ForeignKey(
        to=Scale,
        on_delete=models.CASCADE,
        # related_name="answers",
        # related_query_name="scale",
        verbose_name="Scale",
        null=True,
        blank=True,
    )
    number = models.IntegerField("Answer Number", default=1, blank=True)
    points = models.IntegerField(verbose_name="Answer points", default=1, blank=True)

    class Meta:
        verbose_name = "answer"
        verbose_name_plural = "answers"
        ordering = ["number", "-created_at"]

    def __str__(self):
        return f"{self.question.test.name}'s question #{self.number}"
