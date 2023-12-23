from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from ckeditor.fields import RichTextField
from django_countries.fields import CountryField
from imagekit.models import ImageSpecField

from apps.categories.models import Category
from apps.utils.models import BaseModel


class Brand(BaseModel):
    name = models.CharField("Название", max_length=100)
    slogan = models.CharField("Слоган", max_length=100)
    icon = models.ImageField("Иконка в поиске", upload_to="brands/icons")
    phone = models.IntegerField("Телефон", default=991979899,
                                help_text="Образец: 991979899")
    address = models.CharField("Адрес", max_length=50, default="6A Лабзак, Ташкент")
    email_support = models.CharField("Официальный сайт", default="example.com", max_length=100)
    email = models.EmailField("E-mail для связи", default="example@email.com")
    location_url = models.URLField("Ссылка для локации (Google Maps, Yandex)", null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name="Категория", related_name="brands",
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL)
    country = CountryField(default="UZ")
    description = RichTextField(verbose_name="Описание", null=True, blank=True)
    logo = models.ImageField(verbose_name="Логотип", upload_to="stones/brand")
    logo_thumbnail = ImageSpecField(source='logo',
                                    format='PNG',
                                    options={'quality': 60})
    image = models.ImageField(verbose_name="Изображение", upload_to="stones/brand")
    image_thumbnail = ImageSpecField(source='image',
                                     format='JPEG',
                                     options={'quality': 60})
    order = models.IntegerField(verbose_name="Порядок в списке", default=0)

    class Meta:
        verbose_name = "Бренд "
        verbose_name_plural = "Бренды "

    def __str__(self):
        return self.name


class BrandSocials(models.Model):
    class SocialsChoices(models.TextChoices):
        FB = "fb", "Facebook"
        TG = "tg", "Telegram"
        IG = "ig", "Instagram"
        TW = "tw", "Twitter"
        YT = "yt", "Youtube"
        WA = "wa", "Whatsapp"

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="socials")
    link = models.URLField(verbose_name="Ссылка")
    type = models.CharField(choices=SocialsChoices.choices, default=SocialsChoices.FB, max_length=2)

    class Meta:
        verbose_name = "Ссылка соц сети"
        verbose_name_plural = "Ссылки соц сетей"


class BrandLocations(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="locations")
    long = models.FloatField("Долгота", validators=[MinValueValidator(-180), MaxValueValidator(180)])
    lat = models.FloatField("Широта", validators=[MinValueValidator(-90), MaxValueValidator(90)])

    class Meta:
        verbose_name = "Локация бренда"
        verbose_name_plural = "Локации бренда"


class Categories(BaseModel):
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
    category = models.ForeignKey(Categories, verbose_name="Модель", on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="products")
    brand = models.ForeignKey(Brand, verbose_name="Бренд", on_delete=models.SET_NULL, null=True, blank=True,
                              help_text="Если продукт не имеет модели, вы можете указать бренд",
                              related_name="products")
    name = models.CharField(verbose_name="Название", max_length=100)
    image = models.ImageField(verbose_name="Изображение", upload_to="stones/products")
    image_thumbnail = ImageSpecField(source='image',
                                     format='JPEG',
                                     options={'quality': 60})

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
