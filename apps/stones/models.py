from django.db import models
from ckeditor.fields import RichTextField
from imagekit.models import ImageSpecField


class Brand(models.Model):
    name = models.CharField("Название", max_length=100)
    description = RichTextField(verbose_name="Описание")
    logo = models.ImageField(verbose_name="Логотип")
    logo_thumbnail = ImageSpecField(source='logo',
                                    format='JPEG',
                                    options={'quality': 60})
    image = models.ImageField(verbose_name="Изображение")
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
    image = models.ImageField(verbose_name="Изображение")
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
    image = models.ImageField(verbose_name="Изображение")
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