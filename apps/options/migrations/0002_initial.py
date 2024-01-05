# Generated by Django 4.2.3 on 2024-01-05 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("scales", "0001_initial"),
        ("options", "0001_initial"),
        ("questions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="optionscore",
            name="scale",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="scales.scale",
            ),
        ),
        migrations.AddField(
            model_name="option",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="options",
                related_query_name="option",
                to="questions.question",
                verbose_name="Вопрос",
            ),
        ),
    ]