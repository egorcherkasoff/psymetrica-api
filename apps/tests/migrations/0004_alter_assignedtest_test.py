# Generated by Django 4.2.3 on 2024-01-06 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0003_assignedtest"),
    ]

    operations = [
        migrations.AlterField(
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
