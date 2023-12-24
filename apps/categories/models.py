from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    image = models.ImageField(verbose_name="Изображение", upload_to="categories")
    hide = models.BooleanField(verbose_name="Скрыть из главной?", default=False)
    order = models.IntegerField(verbose_name="Порядковый номер", default=0)

    class Meta:
        verbose_name = "Категория "
        verbose_name_plural = "Категории "

    def __str__(self):
        return self.name


class Table(models.Model):
    name = models.CharField("Название таблицы", max_length=100)
    is_show = models.BooleanField("Показать?", default=True)

    class Meta:
        verbose_name = "Таблица"
        verbose_name_plural = "Таблицы"

    def __str__(self):
        return self.name
