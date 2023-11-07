# Generated by Django 4.2.7 on 2023-11-06 22:35

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
                ("description", ckeditor.fields.RichTextField(verbose_name="Описание")),
                ("logo", models.ImageField(upload_to="", verbose_name="Логотип")),
                ("image", models.ImageField(upload_to="", verbose_name="Изображение")),
            ],
            options={
                "verbose_name": "Бренд ",
                "verbose_name_plural": "Бренды ",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
                ("image", models.ImageField(upload_to="", verbose_name="Изображение")),
                ("arkon_url", models.CharField(max_length=255, verbose_name="Ссылка на AR")),
            ],
        ),
        migrations.CreateModel(
            name="Characteristic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("main", "Основные характеристики"),
                            ("standart", "Стандарты"),
                            ("test", "Характерестики тестов"),
                        ],
                        default="main",
                        max_length=10,
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
                ("value", models.CharField(max_length=100, verbose_name="Значение")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="characteristics",
                        to="stones.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
                ("image", models.ImageField(upload_to="", verbose_name="Изображение")),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="categories",
                        to="stones.brand",
                        verbose_name="Бренд",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория ",
                "verbose_name_plural": "Категории ",
            },
        ),
    ]