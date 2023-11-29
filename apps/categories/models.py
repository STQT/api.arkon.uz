from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    image = models.ImageField(verbose_name="Изображение", upload_to="categories")
    hide = models.BooleanField(verbose_name="Скрыть из главной?", default=False)

    class Meta:
        verbose_name = "Категория "
        verbose_name_plural = "Категории "

    def __str__(self):
        return self.name
