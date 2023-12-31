# Generated by Django 4.2.7 on 2023-11-29 07:39

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("image", models.ImageField(upload_to="categories", verbose_name="Изображение")),
                ("hide", models.BooleanField(default=False, verbose_name="Скрыть из главной?")),
            ],
            options={
                "verbose_name": "Категория ",
                "verbose_name_plural": "Категории ",
            },
        ),
    ]
