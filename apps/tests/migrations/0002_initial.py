# Generated by Django 4.2.3 on 2024-02-13 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tests", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="testpasses",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="passes",
                related_query_name="user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddField(
            model_name="test",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tests",
                related_query_name="test",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
        migrations.AddField(
            model_name="test",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tests",
                to="tests.category",
                verbose_name="категория",
            ),
        ),
        migrations.AddField(
            model_name="assignedtest",
            name="assigned_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assigned_by_tests",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Кто назначил",
            ),
        ),
        migrations.AddField(
            model_name="assignedtest",
            name="assigned_to",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assigned_to_tests",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Кому назначено",
            ),
        ),
        migrations.AddField(
            model_name="assignedtest",
            name="test",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assignments",
                to="tests.test",
                verbose_name="Тест",
            ),
        ),
    ]
