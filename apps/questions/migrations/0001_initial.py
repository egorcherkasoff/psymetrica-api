# Generated by Django 4.2.3 on 2024-01-21 10:27

import apps.questions.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата изменения"),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="Дата удаления",
                    ),
                ),
                (
                    "is_required",
                    models.BooleanField(default=True, verbose_name="Обязательный"),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("single_option", "Вопрос с одним вариантом ответа"),
                            (
                                "multiple_options",
                                "Вопрос с несколькими вариантами ответа",
                            ),
                            ("text", "Вопрос с открытым ответом"),
                            ("range", "Вопрос с диапазоном"),
                            ("image", "Вопрос с выбором из картинок"),
                            ("intro", "Ознакомительный материал"),
                        ],
                        max_length=30,
                        verbose_name="Тип вопроса",
                    ),
                ),
                ("text", models.CharField(max_length=255, verbose_name="Текст")),
                (
                    "number",
                    models.PositiveIntegerField(
                        default=1, verbose_name="Номер вопроса"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        default="avatars/default.svg",
                        upload_to=apps.questions.models.filename_to_uuid,
                        verbose_name="Изображение",
                    ),
                ),
            ],
            options={
                "verbose_name": "вопрос",
                "verbose_name_plural": "вопросы",
                "ordering": ["number", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="QuestionGroup",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата изменения"),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="Дата удаления",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                (
                    "questions",
                    models.ManyToManyField(
                        related_name="groups",
                        to="questions.question",
                        verbose_name="Вопросы",
                    ),
                ),
            ],
            options={
                "verbose_name": "группа вопросов",
                "verbose_name_plural": "группы вопросов",
                "ordering": ["-created_at"],
            },
        ),
    ]
