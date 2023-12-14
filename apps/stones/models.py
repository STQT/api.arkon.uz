from django.db import models
from ckeditor.fields import RichTextField
from imagekit.models import ImageSpecField

from apps.categories.models import Category
from apps.utils.models import BaseModel


class Brand(BaseModel):
    name = models.CharField("Название", max_length=100)
    phone = models.CharField("Телефон", max_length=50, default="+998712020020")
    address = models.CharField("Адрес", max_length=50, default="6A Лабзак, Ташкент")
    email = models.EmailField("E-mail для связи", default="example@email.com")
    email_support = models.EmailField("E-mail для поддержки", default="example@email.com")
    location_url = models.URLField("Ссылка для локации (Google Maps, Yandex)",
                                   default="https://maps.app.goo.gl/XZYYgEisV3hzBaWu5")
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


class Category(BaseModel):
    brand = models.ForeignKey(Brand, verbose_name="Бренд", related_name="categories", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название", max_length=100)
    image = models.ImageField(verbose_name="Изображение", upload_to="stones/categories")
    image_thumbnail = ImageSpecField(source='image',
                                     format='JPEG',
                                     options={'quality': 60})

    class Meta:
        verbose_name = "Модель "
        verbose_name_plural = "Модели "

    def __str__(self):
        return self.name


class Product(BaseModel):
    category = models.ForeignKey(Category, verbose_name="Модель", on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(Brand, verbose_name="Бренд", on_delete=models.SET_NULL, null=True, blank=True,
                              help_text="Если продукт не имеет модели, вы можете указать бренд",
                              related_name="products")
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


class ProductShots(models.Model):
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE, related_name="shots")  # noqa
    image = models.ImageField(verbose_name="Изображение", upload_to="stones/product_shots")
    image_thumbnail = ImageSpecField(source='image',
                                     format='JPEG',
                                     options={'quality': 60})

    class Meta:
        verbose_name = "Изображение продукта "
        verbose_name_plural = "Изображения продукта "

    def __str__(self):
        return self.product.name


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
