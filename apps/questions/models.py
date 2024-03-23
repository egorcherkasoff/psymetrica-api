import uuid

from django.db import models
from django.utils import timezone

from apps.base.models import BaseModel

from ..tests.models import Test


def filename_to_uuid(instance, filename):
    """генерация уникального имени файла"""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"question_images/{filename}"


class Question(BaseModel):
    """модель вопроса"""

    class QuestionTypes(models.TextChoices):
        """содержит типы вопросов"""

        SINGLE_OPTION = (
            "single_option",
            "Вопрос с одним вариантом ответа",
        )
        MULTIPLE_OPTIONS = (
            "multiple_options",
            "Вопрос с несколькими вариантами ответа",
        )
        TEXT = (
            "text",
            "Вопрос с открытым ответом",
        )
        RANGE = (
            "range",
            "Вопрос с диапазоном",
        )
        IMAGE = (
            "image",
            "Вопрос с выбором из картинок",
        )
        MATRIX_SINGLE = (
            "matrix_single",
            "Вопрос с выбором одного ответа по строке",
        )
        MATRIX_MULTI = (
            "matrix_mutli",
            "Вопрос с выбором нескольких ответов по строке",
        )
        # по сути как такогого вопроса нет, используется для вывода какой-либо информации
        INTRO = (
            "intro",
            "Ознакомительный материал",
        )

    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        related_name="questions",
        related_query_name="question",
        verbose_name="Тест",
    )

    is_required = models.BooleanField(default=True, verbose_name="Обязательный")

    type = models.CharField(
        choices=QuestionTypes.choices, verbose_name="Тип вопроса", max_length=30
    )

    text = models.CharField(max_length=255, verbose_name="Текст")

    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=filename_to_uuid,
        verbose_name="Изображение",
    )

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"
        ordering = ["-created_at"]

    # TODO: переделать!
    def __str__(self):
        return f'Вопрос №для теста "{self.test.title}"'

    def get_options(self):
        """возвращает все варианты ответов к тесту"""
        return self.options.filter(deleted_at__isnull=True)

    @property
    def options_count(self):
        """возвращает кол-во вариантов ответов к вопросу"""
        return self.get_options().count()

    def get_image(self):
        """возвращает урл картинки вопроса"""
        return self.image.url if self.image else None

    # TODO: сделать! валидацию, её юзать потом в сериализаторае
    # def clean(self):
    #     """доп валидация для номера вопроса"""
    #     print("validated...")
    #     raise NotImplementedError

    def delete(self):
        """выполняет мягкое удаление вопроса и зависимых моделей (например, варианты ответов)"""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])
        # вызываем delete на каждом из вариантов ответа, если они есть
        options = self.get_options()
        if options:
            for option in options:
                option.delete()


class QuestionBlock(BaseModel):
    """блок вопросов"""

    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        related_name="question_blocks",
        related_query_name="question_block",
        verbose_name="Тест",
    )

    questions = models.ManyToManyField(
        to=Question,
        related_name="question_blocks",
        related_query_name="question_block",
        verbose_name="Вопросы",
    )

    private_title = models.CharField(
        max_length=255, verbose_name="Заголовок (Не отображается пользователю)"
    )

    public_title = models.CharField(
        max_length=255, verbose_name="Заголовок (Отображается пользователю)"
    )

    description = models.CharField(
        max_length=255,
        verbose_name="Описание",
    )

    order = models.PositiveSmallIntegerField(
        verbose_name="Порядок",
        default=1,
    )

    class Meta:
        verbose_name = "блок вопросов"
        verbose_name_plural = "блоки вопросов"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Блок вопросов для теста {self.test.title}"
