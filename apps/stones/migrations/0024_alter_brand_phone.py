# Generated by Django 4.2.7 on 2023-12-23 13:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stones", "0023_alter_brand_location_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brand",
            name="phone",
            field=models.IntegerField(
                default=991979899, help_text="Образец: 991979899", max_length=50, verbose_name="Телефон"
            ),
        ),
    ]
