# Generated by Django 4.2.7 on 2023-11-10 21:20

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
                ("slogan", models.CharField(max_length=50, verbose_name="Девиз")),
                ("logo", models.ImageField(upload_to="mebels/brand", verbose_name="Логотип")),
                ("logo_light", models.ImageField(upload_to="stones/brand", verbose_name="Логотип для светлой версии")),
                ("image", models.ImageField(upload_to="mebels/brand", verbose_name="Изображение")),
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
                ("image", models.ImageField(upload_to="mebels/products", verbose_name="Изображение на главной")),
                (
                    "image2",
                    models.ImageField(
                        blank=True, null=True, upload_to="mebels/products", verbose_name="Изображение на главной 2"
                    ),
                ),
                (
                    "image3",
                    models.ImageField(
                        blank=True, null=True, upload_to="mebels/products", verbose_name="Изображение на главной 3"
                    ),
                ),
                ("arkon_url", models.CharField(max_length=255, verbose_name="Ссылка на AR")),
                (
                    "brend",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="mebels.brand",
                        verbose_name="Бренд",
                    ),
                ),
            ],
            options={
                "verbose_name": "Продукт ",
                "verbose_name_plural": "Продукты ",
            },
        ),
        migrations.CreateModel(
            name="ProductShots",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="mebels/product_shots", verbose_name="Изображение")),
                ("arkon_url", models.CharField(max_length=255, verbose_name="Ссылка на AR")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shots",
                        to="mebels.product",
                        verbose_name="Продукт",
                    ),
                ),
            ],
            options={
                "verbose_name": "Изображение продукта ",
                "verbose_name_plural": "Изображения продукта ",
            },
        ),
    ]