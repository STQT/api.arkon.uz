from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField


class Brand(models.Model):
    name = models.CharField("Название", max_length=100)
    phone = models.CharField("Телефон", max_length=50)
    content = RichTextUploadingField()

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