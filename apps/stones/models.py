from django.db import models
from ckeditor.fields import RichTextField
from imagekit.models import ImageSpecField

from apps.categories.models import Category


class Brand(models.Model):
    name = models.CharField("Название", max_length=100)
    category = models.ForeignKey(Category, verbose_name="Категория", related_name="stones",
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL)
    description = RichTextField(verbose_name="Описание")
    logo = models.ImageField(verbose_name="Логотип", upload_to="stones/brand")
    logo_thumbnail = ImageSpecField(source='logo',
                                    format='PNG',
                                    options={'quality': 60})
    image = models.ImageField(verbose_name="Изображение", upload_to="stones/brand")
    image_thumbnail = ImageSpecField(source='image',
                                     format='JPEG',
                                     options={'quality': 60})

    class Meta:
        verbose_name = "Бренд "
        verbose_name_plural = "Бренды "

    def __str__(self):
        return self.name


class Category(models.Model):
    brand = models.ForeignKey(Brand, verbose_name="Бренд", related_name="categories", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название", max_length=100)
    image = models.ImageField(verbose_name="Изображение", upload_to="stones/categories")
    image_thumbnail = ImageSpecField(source='image',
                                     format='JPEG',
                                     options={'quality': 60})

    class Meta:
        verbose_name = "Категория "
        verbose_name_plural = "Категории "

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE, related_name="products")
    name = models.CharField(verbose_name="Название", max_length=100)
    image = models.ImageField(verbose_name="Изображение", upload_to="stones/products")
    image_thumbnail = ImageSpecField(source='image',
                                     format='JPEG',
                                     options={'quality': 60})
    arkon_url = models.CharField(verbose_name="Ссылка на AR", max_length=255)

    class Meta:
        verbose_name = "Продукт "
        verbose_name_plural = "Продукты "

    def __str__(self):
        return self.name


class Characteristic(models.Model):
    class CharacteristicTypeChoices(models.TextChoices):
        MAIN = "main", "Основные характеристики"
        STANDART = "standart", "Стандарты"
        TEST = "test", "Характерестики тестов"

    type = models.CharField(max_length=10,
                            choices=CharacteristicTypeChoices.choices,
                            default=CharacteristicTypeChoices.MAIN)
    name = models.CharField(max_length=100, verbose_name="Название")
    value = models.CharField(max_length=100, verbose_name="Значение")
    product = models.ForeignKey(Product, related_name='characteristics', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.value}"
