from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum

from apps.base.models import BaseModel

from ..options.models import Option
from ..scales.models import Scale
from ..tests.models import Test

User = get_user_model()


class Attempt(BaseModel):
    """Модель прохождения теста"""

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="attempts",
        related_query_name="attempt",
    )

    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        verbose_name="Тест",
        related_name="attempts",
        related_query_name="attempt",
    )

    ip = models.GenericIPAddressField(
        verbose_name="IP-адрес",
        default="0.0.0.0",
    )

    is_finished = models.BooleanField(
        default=False,
        verbose_name="Прохождение завершено",
    )

    class Meta:
        verbose_name = "попытка"
        verbose_name_plural = "прохождения"
        ordering = ["-created_at"]

    @property
    def is_finished(self):
        return True if self.finished is not None else False

    def __str__(self):
        finished = (
            "Не завершена"
            if self.finished is None
            else f"Завершена на {self.get_finished_date()}"
        )
        return f'Попытка теста "{self.test}" пользователя {self.user} от {self.get_start_date()}. {finished}'

    # TODO: переделать. под чем я был когда это писал
    def get_results(self):
        """возвращает результаты прохождения"""
        if self.is_finished:
            scales = []
            scores = []
            # для каждого объекта attemptanswer считаем сумму баллов по шкалам (если их нет, то возвращаем просто сумму баллов)
            for answer in self.answers.filter(deleted_at__isnull=True):
                scores = (
                    self.answers.filter(deleted_at__isnull=True)
                    .values("scale")
                    .annotate(score=Sum("score"))
                )
                if answer.scale:
                    scales.append(answer.scale)
            return scales, scores
        return None

    def get_unreviewed_answers(self):
        """возвращает вопросы с типом "OPEN", которые не оценены"""
        return self.answers.filter(
            deleted_at__isnull=True,
            answer__isnull=False,
            answer__score=0,
            answer__deleted_at__isnull=True,
        )

    def get_answers(self):
        return self.answers.filter(deleted_at__isnull=True)

    def get_start_date(self):
        return self.created_at.strftime("%d.%m.%Y в %H:%M")

    def get_finished_date(self):
        if self.finished:
            return self.finished.strftime("%d.%m.%Y в %H:%M")
        return "Не завершено"


class AttemptAnswer(BaseModel):
    """Модель ответов прохождения"""

    attempt = models.ForeignKey(
        to=Attempt,
        on_delete=models.CASCADE,
        related_name="answers",
        related_query_name="answer",
    )

    option = models.ForeignKey(
        to=Option,
        on_delete=models.CASCADE,
        related_name="answers",
        related_query_name="answer",
    )

    # поле заполняется только при типе вопроса OPEN или RANGE
    answer = models.CharField(
        max_length=255, verbose_name="Ответ", blank=True, null=True
    )

    # используются для хранения баллов прохождения
    score = models.SmallIntegerField(
        default=0, verbose_name="Баллы"
    )  # выставляется вручую если вопрос типа OPEN

    scale = models.ForeignKey(
        to=Scale, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Шкала"
    )

    class Meta:
        verbose_name = "ответ прохождения"
        verbose_name_plural = "ответы прохождения"
        ordering = ["-attempt", "-created_at"]
        unique_together = ["attempt", "option"]

    def __str__(self):
        return f"Ответ прохождения {self.attempt.id} на {self.option.question}"

    def clean(self):
        if self.option.question.test == self.attempt.test:
            return super().clean()
        raise ValidationError(
            "Этот вариант ответа не существует или отсносится к другому тесту"
        )
