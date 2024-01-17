from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from apps.base.models import BaseModel

User = get_user_model()


class Category(BaseModel):
    """Модель категории"""

    title = models.CharField(db_index=True, max_length=255, verbose_name="Название")
    slug = AutoSlugField(
        always_update=True,
        populate_from="title",
        unique=True,
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_tests(self):
        """возвращает все публичные тесты категории"""
        return self.tests.filter(deleted_at__isnull=True, is_published=True)


class Test(BaseModel):
    """Модель теста"""

    title = models.CharField(db_index=True, max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="tests",
        related_query_name="test",
        verbose_name="Автор",
    )

    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        related_name="tests",
        verbose_name="категория",
        null=True,
        blank=True,
    )

    slug = AutoSlugField(
        always_update=True,
        populate_from="title",
        unique=True,
    )

    # в проде поставить на false, поскольку тесты должны пройти модерацию, чтобы стать публичными
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "тест"
        verbose_name_plural = "тесты"
        ordering = ["-created_at"]

    @property
    def actual_question_count(self):
        """возвращает кол-во вопросов, не являющихся вопросами intro"""
        return self.questions.exclude(
            question__type="intro", deleted_at__isnull=True
        ).count()

    def __str__(self):
        return f'Тест "{self.title}" от пользователя "{self.author}"'

    def get_questions(self):
        """возвращает все вопросы теста"""
        return self.questions.filter(deleted_at__isnull=True)

    def get_scales(self):
        """возвращает все шкалы теста"""
        return self.scales.filter(deleted_at__isnull=True)

    def get_attempts(self):
        """возвращает все попытки теста"""
        return self.attempts.filter(
            deleted_at__isnull=True,
        )

    def get_user_attempts(self, user):
        """возвращает все попытки теста для какого либо пользователя"""
        return self.attempts.filter(deleted_at__isnull=True, user=user)

    def delete(self):
        """выполняет мягкое удаление теста и зависимых моделей (например, вопросы)"""
        self.deleted_at = timezone.now()
        # очевидно, публичные тесты перестают быть такими при удалении.
        self.is_published = False
        self.save(update_fields=["is_published", "deleted_at"])
        questions = self.get_questions()
        # вызываем delete на каждом из вопросов, если они есть
        if questions:
            for question in questions:
                question.delete()


class AssignedTest(BaseModel):
    """Модель назначения теста"""

    assigned_to = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Кому назначено",
        related_name="assigned_to_tests",
    )
    assigned_by = models.ForeignKey(
        related_name="assigned_by_tests",
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Кто назначил",
    )

    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        verbose_name="Тест",
        related_name="assignments",
    )

    def __str__(self):
        return f"{self.test} назначен пользователю {self.assigned_to} в {self.get_created_at()}"

    def get_created_at(self):
        return self.created_at.strftime("%d.%m.%Y в %H:%M")

    class Meta:
        verbose_name = "Назначение теста"
        verbose_name_plural = "Назначения теста"
        ordering = ["assigned_to", "test", "-created_at"]
