# Generated by Django 4.2.3 on 2024-01-04 14:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Attempt",
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
                    "finished",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Дата завершения"
                    ),
                ),
            ],
            options={
                "verbose_name": "попытка",
                "verbose_name_plural": "попытки",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="AttemptAnswers",
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
                    "attempt",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        related_query_name="answer",
                        to="attempts.attempt",
                    ),
                ),
            ],
            options={
                "verbose_name": "ответ попытки",
                "verbose_name_plural": "ответы попытки",
                "ordering": ["-attempt", "-created_at"],
            },
        ),
    ]
