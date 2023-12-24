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
    slogan_color = models.CharField("Цвет слогана", max_length=10, default="#FFFFFF")
    phone = models.IntegerField("Телефон", default=991979899,
                                help_text="Образец: 991979899")
    address = models.CharField("Адрес", max_length=50, default="6A Лабзак, Ташкент")
    product_label = models.CharField(verbose_name="Заголовок блока продуктов", max_length=100,
                                     null=True, blank=True, default="Products")
    category = models.ForeignKey(Category, verbose_name="Категория", related_name="brands",
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL)
    category_label = models.CharField(verbose_name="Заголовок блока коллекций", max_length=100,
                                      null=True, blank=True, default="Collections")
    description = RichTextField(verbose_name="Описание", null=True, blank=True)
    information_label = models.CharField("Заголовок блока информаций", max_length=100,
                                         default="INFORMATION OF COMPANY", null=True, blank=True)
    email_support = models.CharField("Официальный сайт",
                                     default="arkon.uz", max_length=100,
                                     null=True, blank=True)
    email = models.EmailField("E-mail для связи", default="info@arkon.uz", blank=True, null=True)
    location_url = models.URLField("Ссылка для локации (Google Maps, Yandex)", null=True, blank=True)
    country = CountryField(default="UZ")
    icon = models.ImageField("Иконка в поиске", upload_to="brands/icons")
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
    name = models.CharField(verbose_name="Название", max_length=100, blank=True, null=True)
    name_color = models.CharField(verbose_name="Цвет названия", max_length=10, default="#FFFFFF")
    product_label = models.CharField(verbose_name="Заголовок блока продуктов", max_length=10,
                                     null=True, blank=True, default="Products")
    image = models.ImageField(verbose_name="Изображение", upload_to="stones/categories")
    image_thumbnail = ImageSpecField(source='image',
                                     format='JPEG',
                                     options={'quality': 60})

    class Meta:
        verbose_name = "Модель "
        verbose_name_plural = "Модели "

    def __str__(self):
        try:
            return self.name
        except:
            return None


class Product(BaseModel):
    category = models.ForeignKey(Categories, verbose_name="Модель", on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="products")
    brand = models.ForeignKey(Brand, verbose_name="Бренд", on_delete=models.SET_NULL, null=True, blank=True,
                              help_text="Если продукт не имеет модели, вы можете указать бренд",
                              related_name="products")
    name = models.CharField(verbose_name="Название", max_length=100, blank=True, null=True)
    name_color = models.CharField(verbose_name="Цвет названия", max_length=10, default="#FFFFFF")

    image = models.ImageField(verbose_name="Изображение", upload_to="stones/products")
    image_thumbnail = ImageSpecField(source='image',
                                     format='JPEG',
                                     options={'quality': 60})

    class Meta:
        verbose_name = "Продукт "
        verbose_name_plural = "Продукты "

    def __str__(self):
        try:
            return self.name
        except:
            return None


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
    type = models.ForeignKey("categories.Table", on_delete=models.CASCADE, related_name='characteristics')
    name = models.CharField(max_length=100, verbose_name="Название")
    value = models.CharField(max_length=100, verbose_name="Значение")
    product = models.ForeignKey(Product, related_name='characteristics', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.value}"
