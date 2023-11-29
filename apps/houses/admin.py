from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_preview', 'category']

    def logo_preview(self, obj):
        return mark_safe(
            f'<img src="{obj.logo_light.url}" width="200"/>'  # if obj.logo_light else '<div>Rasmsiz</div>'
        )

    logo_preview.short_description = 'Фото'
    logo_preview.allow_tags = True
