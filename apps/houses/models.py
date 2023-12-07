from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField

from apps.categories.models import Category


class Brand(models.Model):
    name = models.CharField("Название", max_length=100)
    phone = models.CharField("Телефон", max_length=50, default="+998712020020")
    address = models.CharField("Адрес", max_length=50, default="6A Лабзак, Ташкент")
    email = models.EmailField("E-mail для связи", default="example@email.com")
    email_support = models.EmailField("E-mail для поддержки", default="example@email.com")
    location_url = models.URLField("Ссылка для локации (Google Maps, Yandex)",
                                   default="https://maps.app.goo.gl/XZYYgEisV3hzBaWu5")
    category = models.ForeignKey(Category, verbose_name="Категория", related_name="houses",
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL)
    content = RichTextUploadingField()

    logo = models.ImageField(verbose_name="Логотип", upload_to="mebels/brand")
    logo_thumbnail = ImageSpecField(source='logo',
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
