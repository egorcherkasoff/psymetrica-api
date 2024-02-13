# Generated by Django 4.2.3 on 2024-02-13 11:58

import apps.options.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ImageOption",
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
                    "image",
                    models.ImageField(
                        upload_to=apps.options.models.filename_to_uuid,
                        verbose_name="Изображение варианта ответа",
                    ),
                ),
            ],
            options={
                "verbose_name": "вариант ответа с картинкой",
                "verbose_name_plural": "варианты ответа с картинкой",
            },
        ),
        migrations.CreateModel(
            name="Option",
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
                    "number",
                    models.PositiveIntegerField(default=1, verbose_name="Номер ответа"),
                ),
            ],
            options={
                "verbose_name": "вариант ответа",
                "verbose_name_plural": "варианты ответа",
                "ordering": ["question", "number", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="TextOption",
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
                    "text",
                    models.CharField(
                        max_length=255, verbose_name="Текст варианта ответа"
                    ),
                ),
                (
                    "option",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="text_option",
                        to="options.option",
                        verbose_name="Вариант ответа",
                    ),
                ),
            ],
            options={
                "verbose_name": "текстовый вариант ответа",
                "verbose_name_plural": "текстовые варианты ответа",
            },
        ),
        migrations.CreateModel(
            name="SingleMatrixOption",
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
                    "text",
                    models.CharField(
                        max_length=255, verbose_name="Текст варианта ответа"
                    ),
                ),
                (
                    "option",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="single_matrix_option",
                        to="options.option",
                        verbose_name="Вариант ответа",
                    ),
                ),
            ],
            options={
                "verbose_name": "вариант ответа на вопрос типа matrix_single",
                "verbose_name_plural": "варианты ответа на вопрос типа matrix_single",
            },
        ),
        migrations.CreateModel(
            name="RangeOption",
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
                ("min_range", models.IntegerField(verbose_name="Минимальный порог")),
                ("max_range", models.IntegerField(verbose_name="Максимальный порог")),
                (
                    "option",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="range_option",
                        to="options.option",
                        verbose_name="Вариант ответа",
                    ),
                ),
            ],
            options={
                "verbose_name": "вариант ответа с картинкой",
                "verbose_name_plural": "варианты ответа с картинкой",
            },
        ),
        migrations.CreateModel(
            name="OptionScore",
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
                ("score", models.SmallIntegerField(default=0, verbose_name="Баллы")),
                (
                    "option",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="scores",
                        to="options.option",
                        verbose_name="Вариант ответа",
                    ),
                ),
            ],
            options={
                "verbose_name": "балл варианта ответа",
                "verbose_name_plural": "баллы вариантов ответа",
            },
        ),
    ]
