from django.db import models
from imagekit.models import ImageSpecField

from apps.categories.models import Category


class Brand(models.Model):
    name = models.CharField("Название", max_length=100)
    category = models.ForeignKey(Category, verbose_name="Категория", related_name="mebels",
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL)
    slogan = models.CharField("Девиз", max_length=50)
    logo = models.ImageField(verbose_name="Логотип", upload_to="mebels/brand")
    logo_thumbnail = ImageSpecField(source='logo',
                                    format='PNG',
                                    options={'quality': 60})
    logo_light = models.ImageField(verbose_name="Логотип для светлой версии", upload_to="stones/brand")
    logo_light_thumbnail = ImageSpecField(source='logo_light',
                                    format='PNG',
                                    options={'quality': 60})
    image = models.ImageField(verbose_name="Изображение", upload_to="mebels/brand")
    image_thumbnail = ImageSpecField(source='image',
                                     format='JPEG',
                                     options={'quality': 60})


    class Meta:
        verbose_name = "Бренд "
        verbose_name_plural = "Бренды "

    def __str__(self):
        return self.name


class Product(models.Model):
    brend = models.ForeignKey(Brand, verbose_name="Бренд", on_delete=models.CASCADE, related_name="products")
    name = models.CharField(verbose_name="Название", max_length=100)
    image = models.ImageField(verbose_name="Изображение на главной", upload_to="mebels/products")
    image_thumbnail = ImageSpecField(source='image',
                                     format='JPEG',
                                     options={'quality': 60})

    image2 = models.ImageField(verbose_name="Изображение на главной 2", upload_to="mebels/products", blank=True, null=True)
    image_thumbnail2 = ImageSpecField(source='image2',
                                     format='JPEG',
                                     options={'quality': 60})

    image3 = models.ImageField(verbose_name="Изображение на главной 3", upload_to="mebels/products", blank=True, null=True)
    image_thumbnail3 = ImageSpecField(source='image3',
                                     format='JPEG',
                                     options={'quality': 60})

    arkon_url = models.CharField(verbose_name="Ссылка на AR", max_length=255)
    is_album = models.BooleanField(verbose_name="Альбомные изображения?",
                                   help_text="Если изображения на странице должны быть показаны "
                                             "как албьомные фото, то отметьте галочкой",
                                   default=True)

    class Meta:
        verbose_name = "Продукт "
        verbose_name_plural = "Продукты "

    def __str__(self):
        return self.name


class ProductShots(models.Model):
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE, related_name="shots")
    image = models.ImageField(verbose_name="Изображение", upload_to="mebels/product_shots")
    image_thumbnail = ImageSpecField(source='image',
                                     format='JPEG',
                                     options={'quality': 60})

    class Meta:
        verbose_name = "Изображение продукта "
        verbose_name_plural = "Изображения продукта "

    def __str__(self):
        return self.product.name
