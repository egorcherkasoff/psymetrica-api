from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone

from apps.base.models import BaseModel, SlimModel
from apps.notifications.models import Notification

User = get_user_model()


class Category(SlimModel):
    """Модель категории"""

    title = models.CharField(
        db_index=True, max_length=255, verbose_name="Название", unique=True
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["title"]

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

    show_results_to_user = models.BooleanField(
        default=True, verbose_name="Показывать результаты пользователю"
    )

    allow_repeated_attempts = models.BooleanField(
        default=False, verbose_name="Разрешено повторное прохождение"
    )

    user_can_go_back = models.BooleanField(
        default=False, verbose_name="Разрешено возвращатся к предыдущему вопросу(ам)"
    )

    # в проде поставить на false, поскольку тесты должны пройти модерацию, чтобы стать публичными
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "тест"
        verbose_name_plural = "тесты"
        ordering = ["-created_at"]
        permissions = [
            ("can_assign_tests", "Может назначать тесты"),
            ("can_crud_tests", "Может добавлять, редактировать, удалять тесты"),
        ]

    @property
    def actual_question_count(self):
        """возвращает кол-во вопросов, не являющихся вопросами intro"""
        return self.questions.exclude(type="intro", deleted_at__isnull=True).count()

    @property
    def total_passes(self):
        """возвращает общее кол-во прохождений(завершенных) теста"""
        return self.passes.all().count()

    @property
    def monthly_passes(self):
        """возвращает кол-во прохождений(завершенных) теста за последний месяц"""
        return self.passes.filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=30)
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
        """возвращает все завершенные попытки теста"""
        return self.attempts.filter(
            deleted_at__isnull=True,
            is_finished=True,
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

    notifications = GenericRelation(Notification)

    def __str__(self):
        return f"{self.test} назначен пользователю {self.assigned_to} в {self.get_created_at()}"

    def get_created_at(self):
        return self.created_at.strftime("%d.%m.%Y в %H:%M")

    class Meta:
        verbose_name = "Назначение теста"
        verbose_name_plural = "Назначения теста"
        ordering = ["assigned_to", "test", "-created_at"]


class TestStartPage(BaseModel):
    """Модель стартовой страницы теста"""

    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        related_name="start_page",
        verbose_name="Тест",
    )

    title = models.CharField(
        db_index=True,
        max_length=255,
        verbose_name="Заголовок",
    )

    description = models.TextField(
        verbose_name="Описание",
        max_length=1024,
    )

    class Meta:
        verbose_name = "Стартовая страница"
        verbose_name_plural = "Стартовые страницы"
        unique_together = ["test"]
        ordering = ["test", "-created_at"]


class TestFinishPage(BaseModel):
    """Модель финальной страницы теста"""

    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        related_name="end_page",
        verbose_name="Тест",
    )

    title = models.CharField(
        db_index=True,
        max_length=255,
        verbose_name="Заголовок",
    )

    description = models.TextField(
        verbose_name="Описание",
        max_length=1024,
    )

    class Meta:
        verbose_name = "Финальная страница"
        verbose_name_plural = "Финальные страницы"
        unique_together = ["test"]
        ordering = ["test", "-created_at"]
