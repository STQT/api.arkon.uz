import os

from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hide = models.BooleanField(default=False, verbose_name="Скрыть?")
    arkon_file = models.FileField(
        default=None, null=True, blank=True,
        verbose_name="Файл AR Iphone",
        help_text="Укажите файл AR для iPhone, если в текущей странице нужно отображать AR")
    arkon_file_android = models.FileField(
        default=None, null=True, blank=True,
        verbose_name="Файл AR Android", help_text="Укажите файл AR для других устройств, "
                                                  "если в текущей странице нужно отображать AR")

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        if self.image:
            # Assuming 'file_field' is the field storing the file
            storage, path = self.image.storage, self.image.path
            if os.path.exists(path):
                storage.delete(path)

        super().delete(*args, **kwargs)
