# Generated by Django 4.2.3 on 2024-01-04 15:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("attempts", "0004_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="attemptanswers",
            name="answer",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Ответ"
            ),
        ),
    ]
