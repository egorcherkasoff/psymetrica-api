# Generated by Django 4.2.3 on 2024-01-16 09:41

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("scales", "0003_scale_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scale",
            name="color",
            field=colorfield.fields.ColorField(
                default="#ff0000",
                image_field=None,
                max_length=25,
                samples=None,
                verbose_name="Цвет",
            ),
        ),
    ]